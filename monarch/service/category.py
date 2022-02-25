from monarch.db.models import Category, User
from monarch.constants import CategoryType,  DEFAULT_INCOME_CATEGORY, DEFAULT_EXPENSE_CATEGORY
from monarch.utils.enum import SimpleEnum


# DEFAULT_INCOME_CATEGORY_NAMES = [
#     'Paychecks',
#     'Interest',
# ]

# DEFAULT_EXPENSE_CATEGORY_NAMES = [
#     'Groceries',
#     'Restaurants',
#     'Entertainment',
#     'Travel',
#     'Bills',
#     'Gas',
#     'Shopping',
# ]


# class DEFAULT_INCOME_CATEGORIES(SimpleEnum):
#     PAYCHECKS = 'Paychecks'
#     INTEREST = 'Interest'


# class DEFAULT_EXPENSE_CATEGORIES(SimpleEnum):
#     GROCERIES = 'Groceries'
#     RESTAURANTS = 'Restaurants'
#     ENTERTAINMENT = 'Entertainment'
#     TRAVEL = 'Travel'
#     BILLS = 'Bills',
#     GAS = 'Gas'
#     SHOPPING = 'Shopping'



def create_category(user: User, name: str, type: str):
    assert type in CategoryType

    return Category.objects.create(
        user=user,
        name=name,
        type=type,
    )


def create_default_categories_for_user(user: User):
    for name in DEFAULT_INCOME_CATEGORY:
        create_category(user=user, name=name, type=CategoryType.INCOME)
    for name in DEFAULT_EXPENSE_CATEGORY:
        create_category(user=user, name=name, type=CategoryType.EXPENSE)


def get_user_category_by_name(user: User, name: str):
    return user.categories.get(name=name)
