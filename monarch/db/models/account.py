from django.db import models


class Account(models.Model):
    class Meta:
        db_table = "account"

    data_provider_id = models.TextField(blank=True, null=True, unique=True)

    # Primary data
    name = models.TextField(blank=True, null=True)  # only non-blank when user edited name
    type = models.TextField(null=True)

    # current_balance = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)

    user = models.ForeignKey(
        "monarch.User",
        related_name="accounts",
        on_delete=models.CASCADE,
    )
