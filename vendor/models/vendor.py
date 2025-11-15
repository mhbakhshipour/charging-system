from django.db import models

from charging_system_b2b.utils.models.base_model import BaseModel


class Vendor(BaseModel):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    current_balance = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return f"{self.name}"
