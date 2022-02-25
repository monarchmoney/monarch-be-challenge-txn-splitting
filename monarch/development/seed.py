from datetime import date

from monarch.db.models import User
from monarch.constants import AccountType, DEFAULT_EXPENSE_CATEGORY, DEFAULT_INCOME_CATEGORY
from monarch.service.account import create_account
from monarch.service.category import create_default_categories_for_user, get_user_category_by_name
from monarch.service.transaction import create_transaction


def reset_data_for_user(user: User):
    user.transactions.all().delete()
    user.accounts.all().delete()
    user.categories.all().delete()


def seed_data_for_user(user: User, reset=True):
    if reset:
        reset_data_for_user(user)

    create_default_categories_for_user(user)

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

    seed_credit_transactions(credit_account)
    seed_checking_transactions(checking_account)


CREDIT_TRANSACTIONS = [
    ("Netflix", -14.99, date(2022, 1, 15), DEFAULT_EXPENSE_CATEGORY.ENTERTAINMENT),
    ("Netflix", -14.99, date(2022, 2, 15), DEFAULT_EXPENSE_CATEGORY.ENTERTAINMENT),
    ("Amici's Pizza", -54.26, date(2022, 1, 18), DEFAULT_EXPENSE_CATEGORY.ENTERTAINMENT),
    ("Safeway", -34.53, date(2022, 1, 22), DEFAULT_EXPENSE_CATEGORY.GROCERIES),
]

CHECKING_TRANSACTIONS = [
    ("Acme Corp Paycheck", 1500, date(2022, 1, 15), DEFAULT_INCOME_CATEGORY.PAYCHECKS),
    ("Acme Corp Paycheck", 1500, date(2022, 1, 30), DEFAULT_INCOME_CATEGORY.PAYCHECKS),

]


def _create_transactions_from_values(account, values):
    user = account.user
    for (description, amount, dt, category_name) in values:
        category = get_user_category_by_name(user=user, name=category_name)
        create_transaction(
            account=account,
            amount=amount,
            date=dt,
            description=description,
            category=category,
        )


def seed_credit_transactions(account):
    _create_transactions_from_values(account, CREDIT_TRANSACTIONS)

def seed_checking_transactions(account):
    _create_transactions_from_values(account, CHECKING_TRANSACTIONS)
