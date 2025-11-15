from django.db import transaction, models

from vendor.models import Vendor
from transaction.services import TransactionService


class VendorCreditService:

    @staticmethod
    @transaction.atomic
    def increase_credit(vendor: Vendor, amount: int):
        vendor = vendor.__class__.objects.select_for_update().get(pk=vendor.id)

        vendor.current_balance = models.F("current_balance") + amount
        vendor.save(update_fields=["current_balance"])

        TransactionService.add_transaction(vendor=vendor, amount=amount)

        return vendor

    @staticmethod
    @transaction.atomic
    def decrease_credit(vendor_id: int, amount: int):
        vendor = Vendor.objects.select_for_update().get(pk=vendor_id)

        vendor.current_balance = models.F("current_balance") - amount
        vendor.save(update_fields=["current_balance"])

        TransactionService.add_transaction(vendor=vendor, amount=amount)

        return vendor
