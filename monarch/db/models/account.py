from django.db import models


from monarch.db.utils import enum_to_choices
from monarch.constants import AccountType


class Account(models.Model):
    class Meta:
        db_table = "account"

    user = models.ForeignKey(
        "monarch.User",
        related_name="accounts",
        on_delete=models.CASCADE,
    )

    data_provider_id = models.TextField(blank=True, null=True, unique=True)

    # Primary data
    name = models.TextField(blank=True, null=True)
    type = models.TextField(choices=enum_to_choices(AccountType), null=True)

    # current_balance = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
