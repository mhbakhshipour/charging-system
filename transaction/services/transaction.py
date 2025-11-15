from django.db import transaction

from transaction.models import Transaction
from transaction.tasks import update_current_balance_task
from vendor.models import Vendor
from customer.models import Customer


class TransactionService:

    @staticmethod
    @transaction.atomic
    def add_transaction(vendor: Vendor, amount: int, customer: Customer = None):
        new_transaction = Transaction.objects.create(
            vendor=vendor,
            customer=customer,
            amount=amount,
        )

        update_current_balance_task.delay(new_transaction.id)

        return new_transaction
