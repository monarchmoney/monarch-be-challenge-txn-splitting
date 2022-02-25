from monarch.db.models import User, Account, Transaction
from monarch.constants import AccountType
from monarch.service.account import create_account


def seed_account_data_for_user(user: User):
    credit_account = create_account(
        user=user,
        name="Chase Sapphire Preferred",
        type=AccountType.CREDIT_CARD,
    )
    checking_account = create_account(
        user=user,
        name="Chase High Yield Checking",
        type=AccountType.CHECKING
    )


def seed_credit_transactions(account):
    pass


def seed_checking_transactions(account):
    pass
