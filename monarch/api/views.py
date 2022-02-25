from django.http import HttpResponseForbidden, Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from monarch.api.serializers import (
    UserSerializer,
    AccountSerializer,
    TransactionSerializer,
    CategorySerializer,
)
from monarch.db.models import User, Account, Category, Transaction
from monarch.service.account import get_account_for_user, get_accounts_for_user
from monarch.service.category import get_categories_for_user, get_category_for_user
from monarch.service.transaction import get_transaction_for_user, get_transactions, update_transaction
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
