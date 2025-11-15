from django.db import transaction

from transaction.services import TransactionService

from vendor.models import Vendor
from customer.models import Customer


class CustomerService:

    @staticmethod
    @transaction.atomic
    def increase_credit(vendor: Vendor, amount: int, customer: Customer):
        if not vendor.current_balance >= amount:
            raise ValueError(
                "Vendor does not have enough balance to increase customer credit."
            )

        vendor_transaction = TransactionService.add_transaction(
            vendor=vendor,
            amount=-amount,
        )
        customer_transaction = TransactionService.add_transaction(
            vendor=vendor,
            customer=customer,
            amount=amount,
        )

        return customer_transaction
