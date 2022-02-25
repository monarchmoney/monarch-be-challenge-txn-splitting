from monarch.utils.enum import SimpleEnum


class AccountType(SimpleEnum):
    CREDIT_CARD = 'credit_card'
    CHECKING = 'checking'
    SAVINGS = 'savings'


class CategoryType(SimpleEnum):
    INCOME = 'income'
    EXPENSE = 'expense'
    TRANSFER = 'tranfer'


class DEFAULT_INCOME_CATEGORY(SimpleEnum):
    PAYCHECKS = 'Paychecks'
    INTEREST = 'Interest'


class DEFAULT_EXPENSE_CATEGORY(SimpleEnum):
    GROCERIES = 'Groceries'
    RESTAURANTS = 'Restaurants'
    ENTERTAINMENT = 'Entertainment'
    TRAVEL = 'Travel'
    BILLS = 'Bills',
    GAS = 'Gas'
    SHOPPING = 'Shopping'
