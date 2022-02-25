from django.db import models


class Category(models.Model):
    class Meta:
        db_table = "category"
        unique_together = ("user", "name")

    user = models.ForeignKey(
        "monarch.User",
        related_name="categories",
        on_delete=models.CASCADE,
    )

    name = models.TextField()
