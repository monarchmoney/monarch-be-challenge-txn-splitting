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
