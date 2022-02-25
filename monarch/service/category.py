from monarch.db.models import Category, User
from monarch.constants import CategoryType,  DEFAULT_INCOME_CATEGORY, DEFAULT_EXPENSE_CATEGORY


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


def get_category_for_user(user, category_id):
    return user.categories.get(id=category_id)


def get_categories_for_user(user):
    return list(user.categories.all())
