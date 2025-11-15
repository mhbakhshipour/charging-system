from django.db import models

from charging_system_b2b.utils.models.base_model import BaseModel


class RequestCredit(BaseModel):
    class RequestCreditStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"

    requester = models.ForeignKey(
        "vendor.Vendor",
        on_delete=models.PROTECT,
        related_name="request_credits",
        db_index=True,
    )
    amount = models.PositiveBigIntegerField()
    status = models.CharField(
        max_length=15,
        choices=RequestCreditStatus.choices,
        default=RequestCreditStatus.PENDING,
    )

    def __str__(self):
        return f"{self.requester} - {self.amount} - {self.status}"

    def save(self, *args, **kwargs):
        if self.pk and self.status == self.RequestCreditStatus.CONFIRMED:
            self.update_current_balance(self)
        super().save(*args, **kwargs)

    def update_current_balance(self):
        if self.status == self.RequestCreditStatus.CONFIRMED:
            vendor = self.requester
            vendor.current_balance = models.F("current_balance") + self.amount
            vendor.save(update_fields=["current_balance"])
