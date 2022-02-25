from django.db import models


class Transaction(models.Model):
    class Meta:
        db_table = "transaction"
        unique_together = ("account", "data_provider_id")

    account = models.ForeignKey(
        "monarch.Account",
        related_name="transactions",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        "monarch.User",
        related_name="transactions",
        on_delete=models.CASCADE,
    )
    data_provider_id = models.TextField(blank=True, null=True)

    # Primary data
    description = models.TextField(blank=True, null=True)  # only non-blank when user edited name
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(
        "monarch.Category",
        related_name="transactions",
        on_delete=models.PROTECT,
        null=True,
    )
