from monarch.db.models import User, Account


def create_account(user: User, name: str, type: str) -> Account:
    """
    Create an account for the user.
    """
    account = Account(
        user=user,
        name=name,
        type=type,
    )
    account.save()
    return account


def get_account_for_user(user, account_id):
    return user.accounts.get(id=account_id)


def get_accounts_for_user(user):
    return list(user.accounts.all())
