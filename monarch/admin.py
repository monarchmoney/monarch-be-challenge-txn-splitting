from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from monarch.db.models import User, Account, Category, Transaction

admin.site.register(User)
admin.site.register(Account)
admin.site.register(Category)
admin.site.register(Transaction)
