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
    return user.accounts.all()


def get_category_for_user(user, category_id):
    if category_id:
        return user.categories.get(id=category_id)


def get_account_by_id(account_id):
    return Account.objects.get(id=account_id)
