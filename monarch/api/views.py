from django.http import HttpResponseForbidden, Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from monarch.api.serializers import (
    UserSerializer,
    AccountSerializer,
    TransactionSerializer,
    CategorySerializer,
)
from monarch.db.models import Account, Category, Transaction
from monarch.service.account import get_account_for_user, get_accounts_for_user
from monarch.service.category import get_categories_for_user, get_category_for_user
from monarch.service.split_transaction import validate_amount, create_transactions, delete_transactions, \
    update_or_create
from monarch.service.transaction import get_transaction_for_user, get_transactions, update_transaction, \
    get_split_transactions, do_transaction_split, undo_transaction_split
from monarch.utils import pick_keys


class UserMe(APIView):
    def get(self, request, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class AccountList(APIView):
    def get(self, request, **kwargs):
        user = request.user
        accounts = get_accounts_for_user(user)

        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)


class AccountDetail(APIView):
    def get_object(self, pk, user):
        try:
            return get_account_for_user(user, pk)
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, pk, **kwargs):
        account = self.get_object(pk, user=request.user)
        serializer = AccountSerializer(account)
        return Response(serializer.data)


class AccountTransactionlist(APIView):
    def get(self, request, pk, **kwargs):
        user = request.user
        account = get_account_for_user(user, pk)
        transactions = get_transactions(account=account)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class CategoryList(APIView):
    def get(self, request, **kwargs):
        user = request.user
        categories = get_categories_for_user(user)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryDetail(APIView):
    def get_object(self, pk, user):
        try:
            return get_category_for_user(user, pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk, **kwargs):
        category = self.get_object(pk, user=request.user)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


class TransactionList(APIView):
    def get(self, request, **kwargs):
        user = request.user
        transactions = get_transactions(user=user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class TransactionDetail(APIView):
    def get_object(self, pk, user):
        try:
            return get_transaction_for_user(user, pk)
        except Transaction.DoesNotExist:
            raise Http404

    def get(self, request, pk, **kwargs):
        transaction = self.get_object(pk, user=request.user)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    def patch(self, request, pk, **kwargs):
        transaction = self.get_object(pk, user=request.user)

        data = request.data
        update_fields = pick_keys(
            request.data, ('description', 'amount', 'date')
        )
        category_id = data.get('category_id')
        if category_id:
            update_fields['category'] = get_category_for_user(request.user, category_id)

        transaction = update_transaction(transaction, **update_fields)

        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)


class SplitTransaction(APIView):

    @staticmethod
    def get_original_transaction(pk, user):
        try:
            return get_transaction_for_user(user, pk)
        except Transaction.DoesNotExist:
            raise Http404

    def get_split_transaction(self, pk, user):
        transaction = self.get_original_transaction(pk, user=user)
        split_transactions = get_split_transactions(pk)
        transaction_serializer = TransactionSerializer(transaction)
        split_serializer = TransactionSerializer(split_transactions, many=True)
        return {"original": transaction_serializer.data,
                "split": split_serializer.data}

    def get(self, request, pk, **kwargs):
        return Response(self.get_split_transaction(pk, request.user))

    def post(self, request, pk, **kwargs):
        original_transaction = self.get_original_transaction(pk, request.user)
        split_transactions = request.data

        validate_amount(original_transaction.amount, split_transactions)
        create_transactions(request.user, split_transactions, original_transaction.date,
                            original_transaction.id, original_transaction.account_id)

        do_transaction_split(original_transaction)

        return Response(self.get_split_transaction(pk, request.user))

    def delete(self, request, pk, **kwargs):
        original_transaction = self.get_original_transaction(pk, user=request.user)
        split_transactions = get_split_transactions(pk)
        delete_transactions(split_transactions)
        undo_transaction_split(original_transaction)
        serializer = TransactionSerializer(original_transaction)
        return Response(serializer.data)

    def patch(self, request, pk, **kwargs):
        original_transaction = self.get_original_transaction(pk, request.user)
        new_split = request.data

        validate_amount(original_transaction.amount, new_split)
        current_split = list(get_split_transactions(pk))
        update_or_create(request.user, original_transaction, current_split, new_split)

        return Response(self.get_split_transaction(pk, request.user))
