from datetime import date
from decimal import Decimal

from rest_framework.exceptions import ValidationError

from monarch.service.account import get_account_by_id
from monarch.service.category import get_category_for_user
from monarch.service.transaction import create_transaction, delete, update_transaction
from monarch.utils import pick_keys


def validate_amount(original_amount, transactions):
    split_amount_sum = round(sum([Decimal(item['amount']) for item in transactions]), 2)

    if round(original_amount, 2) != split_amount_sum:
        raise ValidationError(f'The transactions sum not match with the original transaction '
                              f'value which is ${original_amount}')


def get_category_id(user, received_split):
    """
    Function created to extract the category_id from received data.
    If by any chance the request was made sending the entire category object we are prepared.
    """
    category_id = received_split.get('category_id')
    if category_id:
        return get_category_for_user(user, category_id)
    else:
        category = received_split.get('category')
        if category:
            return get_category_for_user(user, category.get('id'))


def parsed_fields(user, received_data, transaction_date=date, original_id=None, account_id=None):
    fields = pick_keys(received_data, ('description', 'amount'))
    fields['date'] = transaction_date

    category = get_category_id(user, received_data)
    if category:
        fields['category'] = category

    if original_id:
        fields['original_id'] = original_id

    if account_id:
        fields['account'] = get_account_by_id(account_id)

    return fields


def create_transactions(user, transactions_list, transaction_date, original_id=None, account_id=None):
    for transaction in transactions_list:
        fields = parsed_fields(user, transaction, transaction_date,
                               original_id, account_id)

        create_transaction(**fields)


def delete_transactions(transactions_list):
    for transaction in transactions_list:
        delete(transaction.id)


def update_or_create(user, original_transaction, current_split, new_split):
    updated_received = []
    updated_from_db = []
    for current_index, current in enumerate(current_split):
        new_data = next((x for x in new_split if str(x.get('id', None)) == str(current.id)), None)
        if new_data:
            fields = parsed_fields(user, new_data, original_transaction.date)
            update_transaction(current, **fields)

            updated_from_db.append(current)
            updated_received.append(new_data)

    to_delete = [item for item in current_split if item not in updated_from_db]
    delete_transactions(to_delete)

    to_create = [item for item in new_split if item not in updated_received]
    create_transactions(user, to_create, original_transaction.date,
                        original_transaction.id, original_transaction.account_id)


