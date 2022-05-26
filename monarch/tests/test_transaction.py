from datetime import date, timedelta
from decimal import Decimal

import pytest

from monarch.constants import AccountType, CategoryType
from monarch.db.models import User
from monarch.service.account import create_account
from monarch.service.category import create_category
from monarch.service.transaction import create_transaction, get_transactions, delete, get_split_transactions, \
    do_transaction_split, undo_transaction_split, update_transaction

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


def test_create_transaction():
    user = User.objects.create(email='foo@gmail.com', password='password')
    account = create_account(
        user=user,
        name="Chase High Yield Checking",
        type=AccountType.CHECKING
    )
    transaction_date = date.today()
    amount = Decimal('-1500.0')
    description = "Description"
    is_split = True
    output = create_transaction(account, amount, transaction_date, description, is_split=is_split)
    assert output.amount == amount
    assert output.description == description
    assert output.date == transaction_date


def test_get_transactions_should_not_return_the_original(original_transaction):
    create_transaction(
        account=original_transaction.account,
        amount=Decimal('-1000.0'),
        date=original_transaction.date,
        description="Splitted Transaction 1",
        original_id=original_transaction.id
    )

    create_transaction(
        account=original_transaction.account,
        amount=Decimal('-500.0'),
        date=original_transaction.date,
        description="Splitted Transaction 2",
        original_id=original_transaction.id
    )
    transactions = get_transactions(original_transaction.account, original_transaction.account.user)
    ids = [item.id for item in transactions]
    assert len(transactions) == 2
    assert original_transaction.id not in ids


def test_delete_transaction(original_transaction):
    split_1 = create_transaction(
        account=original_transaction.account,
        amount=Decimal('-500.0'),
        date=original_transaction.date,
        description="Splitted Transaction 2",
        original_id=original_transaction.id
    )

    delete(split_1.id)
    split_transactions = list(get_split_transactions(original_transaction.id))
    assert len(split_transactions) == 0


def test_do_and_undo_transaction_split(original_transaction):
    output = do_transaction_split(original_transaction)
    output.is_split = True

    output = undo_transaction_split(original_transaction)
    output.is_split = False


def test_update_transaction(original_transaction):
    splitted_1 = create_transaction(
        account=original_transaction.account,
        amount=Decimal('-1000.0'),
        date=original_transaction.date,
        description="Splitted Transaction 1",
        original_id=original_transaction.id,
    )
    new_date = date.today() + timedelta(days=10)
    new_category = create_category(user=original_transaction.account.user, name="category", type=CategoryType.EXPENSE)
    new_description = "Transaction Description 2"
    new_amount = Decimal('-2000.0')
    new_fields = {"id": splitted_1.id,
                  "description": new_description,
                  "amount": new_amount,
                  "category": new_category,
                  "date": new_date
                  }

    output = update_transaction(splitted_1, **new_fields)
    assert output.date == new_date
    assert output.description == new_description
    assert output.amount == new_amount
