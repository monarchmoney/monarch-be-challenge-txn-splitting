from datetime import date
from decimal import Decimal
from unittest.mock import patch

import pytest
from rest_framework.exceptions import ValidationError

from monarch.constants import AccountType
from monarch.db.models import User, Account, Category
from monarch.service.account import create_account
from monarch.service.split_transaction import validate_amount, parsed_fields, create_transactions, \
    delete_transactions, update_or_create
from monarch.service.transaction import get_split_transactions, create_transaction, get_transaction_by_id

pytestmark = pytest.mark.usefixtures("db")


@pytest.fixture(scope='function')
def original_transaction():
    user = User.objects.create(email='foo@gmail.com', password='password')
    account = create_account(
        user=user,
        name="Chase High Yield Checking",
        type=AccountType.CHECKING
    )
    transaction_date = date.today()
    original_transaction = create_transaction(
        account=account,
        amount=Decimal('-1500.0'),
        date=transaction_date,
        description="Original Transaction",
        is_split=True
    )
    yield original_transaction


def test_validate_amount_should_return_success():
    original_amount = Decimal('-14.99')
    transactions = [{'amount': Decimal('-4.99')},
                    {'amount': Decimal('-10.00')}]
    try:
        validate_amount(original_amount, transactions)
    except Exception as exc:
        assert False, f"'test_validate_amount_should_return_success' raised an exception {exc}"


def test_validate_amount_should_return_raise_exception():
    original_amount = Decimal('-14.99')
    transactions = [{'amount': Decimal('-4.99')},
                    {'amount': Decimal('-10.09')}]
    with pytest.raises(ValidationError):
        validate_amount(original_amount, transactions)


@patch('monarch.service.split_transaction.get_account_by_id')
@patch('monarch.service.split_transaction.get_category_for_user')
def test_parse_fields_test_should_return_full_data(get_category_for_user, get_account_by_id):
    user = User()

    account = Account()
    get_account_by_id.return_value = account

    category = Category(id=1, name="category")
    get_category_for_user.return_value = category

    received_data = {
        "description": "Transaction Description",
        "amount": Decimal('10.5'),
        "category_id": "5"
    }
    transaction_date = date.today()
    original_id = 1
    account_id = 12
    output = parsed_fields(user, received_data, transaction_date, original_id, account_id)

    expected = {
        "description": "Transaction Description",
        "amount": Decimal('10.5'),
        "original_id": 1,
        "date": transaction_date,
        "account": account,
        "category": category
    }
    assert output == expected


def test_create_transactions():
    user = User.objects.create(email='foo@gmail.com', password='password')
    account = create_account(
        user=user,
        name="Chase High Yield Checking",
        type=AccountType.CHECKING
    )

    original_id = 1
    transaction_date = date.today()

    transactions_list = [{
        "description": "Transaction 1",
        "amount": Decimal('10.5')}]

    try:
        create_transactions(user, transactions_list, transaction_date, original_id, account.id)
    except Exception as exc:
        assert False, f"'test_create_transactions' raised an exception {exc}"


def test_delete_transactions():
    user = User.objects.create(email='foo@gmail.com', password='password')
    account = create_account(
        user=user,
        name="Chase High Yield Checking",
        type=AccountType.CHECKING
    )

    original_id = 123
    transaction_date = date.today()

    transactions_list = [{
        "description": "Transaction 1",
        "amount": Decimal('10.5')}]

    create_transactions(user, transactions_list, transaction_date, original_id, account.id)
    saved_transactions = list(get_split_transactions(original_id))
    assert len(saved_transactions) == 1
    delete_transactions(saved_transactions)
    saved_transactions = list(get_split_transactions(original_id))
    assert len(saved_transactions) == 0


def test_update_or_create_should_update_split(original_transaction):
    splitted_1 = create_transaction(
        account=original_transaction.account,
        amount=Decimal('-1000.0'),
        date=original_transaction.date,
        description="Splitted Transaction 1",
        original_id=original_transaction.id,
    )
    splitted_2 = create_transaction(
        account=original_transaction.account,
        amount=Decimal('-500.0'),
        date=original_transaction.date,
        description="Splitted Transaction 2",
        original_id=original_transaction.id
    )

    current_splitted = [splitted_1, splitted_2]
    new_splitted = [{"id": splitted_1.id,
                     "description": "Transaction Description 2",
                     "amount": Decimal('-900.0')},
                    {"id": splitted_2.id,
                     "description": "Transaction Description 2",
                     "amount": Decimal('-600.0')}]

    update_or_create(original_transaction.account.user, original_transaction, current_splitted, new_splitted)
    updated_transaction = get_transaction_by_id(splitted_1.id)
    assert updated_transaction.description == "Transaction Description 2"
    assert updated_transaction.amount == Decimal('-900.0')


def test_update_or_create_should_do_all_options(original_transaction):
    splitted_1 = create_transaction(
        account=original_transaction.account,
        amount=Decimal('-1000.0'),
        date=original_transaction.date,
        description="Splitted Transaction 1",
        original_id=original_transaction.id,
    )
    splitted_2 = create_transaction(
        account=original_transaction.account,
        amount=Decimal('-500.0'),
        date=original_transaction.date,
        description="Splitted Transaction 2",
        original_id=original_transaction.id
    )

    current_splitted = [splitted_1, splitted_2]
    new_splitted = [{"id": splitted_1.id,
                     "description": "Transaction Description 2",
                     "amount": Decimal('-900.0')},
                    {"description": "Transaction Description 3, will be created",
                     "amount": Decimal('-600.0')}]

    update_or_create(original_transaction.account.user, original_transaction, current_splitted, new_splitted)
    saved_transactions = list(get_split_transactions(original_transaction.id))
    assert len(saved_transactions) == 2

    saved_ids = [item.id for item in saved_transactions]
    assert splitted_2.id not in saved_ids

