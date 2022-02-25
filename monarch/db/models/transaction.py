from django.db import models


class Transaction(models.Model):
    class Meta:
        db_table = "transaction"

    data_provider_id = models.TextField(blank=True, null=True, unique=True)

    # Primary data
    description = models.TextField(blank=True, null=True)  # only non-blank when user edited name
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    date = models.DateField()
    # category = models.ForeignKey(
    #     "monarch.Category",
    #    related_name="transactions",
    #    on_delete=models.PROTECT,
    # )

    user = models.ForeignKey(
        "monarch.User",
        related_name="transactions",
        on_delete=models.CASCADE,
    )
    account = models.ForeignKey(
        "monarch.Account",
        related_name="transactions",
        on_delete=models.CASCADE,
    )
