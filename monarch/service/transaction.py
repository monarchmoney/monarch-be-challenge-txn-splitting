from datetime import date
from decimal import Decimal
from typing import Union, Optional

from monarch.db.models import Account, Transaction, Category
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
