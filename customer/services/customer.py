from django.db import transaction

from transaction.models import Transaction
from vendor.models import Vendor
from customer.models import Customer


class CustomerService:

    @staticmethod
    @transaction.atomic
    def increase_credit(vendor: Vendor, amount: int, customer: Customer):
        new_transaction = Transaction.objects.create(
            vendor=vendor,
            customer=customer,
            amount=amount,
        )

        return new_transaction
