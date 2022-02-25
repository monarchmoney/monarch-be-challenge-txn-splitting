from django.db import models

from monarch.constants import CategoryType
from monarch.db.utils import enum_to_choices


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
    type = models.TextField(choices=enum_to_choices(CategoryType))  # 'income', 'expense', 'transfer

    def __str__(self) -> str:
        return f"{self.id} ({self.name})"
