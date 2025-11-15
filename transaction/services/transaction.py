from django.db import transaction, models

from transaction.models import Transaction
from transaction.tasks import update_current_balance_task
from vendor.models import Vendor
from customer.models import Customer


class TransactionService:

    @staticmethod
    @transaction.atomic
    def add_transaction(vendor: Vendor, amount: int, customer: Customer = None):
        if customer is None:
            locked_vendor = Vendor.objects.select_for_update().get(pk=vendor.pk)
            new_transaction = Transaction.objects.create(
                vendor=locked_vendor,
                customer=None,
                amount=amount,
            )
            Vendor.objects.filter(pk=locked_vendor.pk).update(
                current_balance=models.F("current_balance") + amount
            )
            return new_transaction
        else:
            locked_customer = Customer.objects.select_for_update().get(pk=customer.pk)
            new_transaction = Transaction.objects.create(
                vendor=vendor,
                customer=locked_customer,
                amount=amount,
            )
            Customer.objects.filter(pk=locked_customer.pk).update(
                current_balance=models.F("current_balance") + amount
            )
            return new_transaction
