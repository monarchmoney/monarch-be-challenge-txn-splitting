from datetime import date
from decimal import Decimal
from typing import Union, Optional

from monarch.db.models import Account, Transaction, Category, User
from monarch.utils import ensure_decimal


def create_transaction(
    account: Account,
    amount: Union[Decimal, float, str],
    date: date,
    description: str,
    category: Optional[Category] = None,
) -> Transaction:
    """
    Create a transaction
    """
    user = account.user

    amount = ensure_decimal(amount)

    transaction = Transaction(
        user=user,
        account=account,
        amount=amount,
        date=date,
        description=description,
        category=category,
    )
    transaction.save()
    return transaction


def get_transaction_for_user(user, transaction_id):
    return user.transactions.get(id=transaction_id)


def get_transactions(
    account: Optional[Account] = None,
    user: Optional[User] = None,
    offset=0,
    limit=100,
) -> list[Transaction]:
    """
    Get all transactions for an account
    """
    assert account or user

    qs = Transaction.objects

    if account:
        qs = qs.filter(account=account)
    if user:
        qs = qs.filter(user=user)

    qs = qs.order_by('-date')
    transactions = qs.all()[offset: offset + limit]
    return transactions


def update_transaction(
    transaction: Transaction,
    **fields,
) -> Transaction:
    """
    Update a transaction
    """
    if 'description' in fields:
        transaction.description = fields['description']
    if 'amount' in fields:
        transaction.amount = ensure_decimal(fields['amount'])
    if 'date' in fields:
        transaction.date = fields['date']
    if 'category' in fields:
        transaction.category = fields['category']

    transaction.save()
    return transaction
