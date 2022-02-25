from datetime import date
from decimal import Decimal

from monarch.db.models import Account, Transaction

def create_tranaction_for_account(account: Account, amount: Decimal, date: date, description: str) -> Transaction:
    """
    Create a transaction for the user.
    """
    user = account.user

    transaction = Transaction(
        user=user,
        account=account,
        amount=amount,
        date=date,
        description=description,
    )
    transaction.save()
    return transaction
