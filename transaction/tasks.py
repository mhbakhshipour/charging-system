from django.db import transaction, models
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from charging_system_b2b.utils.celery import RedlockedTask

from charging_system_b2b.celery import app


from transaction.models.transaction import Transaction


logger = get_task_logger(__name__)


@app.task(
    name="update_current_balance_task",
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 10, "countdown": 5},
)
def update_current_balance_task(self, transaction_id: int):
    new_transaction = Transaction.objects.select_related("vendor", "customer").get(
        id=transaction_id
    )

    is_vendor_credit = new_transaction.is_vendor_credit

    try:
        with transaction.atomic():
            if is_vendor_credit:
                new_transaction.vendor.current_balance = (
                    models.F("current_balance") + new_transaction.amount
                )
                new_transaction.vendor.save(update_fields=["current_balance"])
            else:
                new_transaction.customer.current_balance = (
                    models.F("current_balance") - new_transaction.amount
                )
                new_transaction.customer.save(update_fields=["current_balance"])
    except Exception as e:
        logger.error(
            f"Failed to update current balance for {'vendor' if is_vendor_credit else 'customer'} "
            f"ID: {new_transaction.vendor.id if is_vendor_credit else new_transaction.customer.id} "
            f"with transaction ID: {new_transaction.id}. Error: {str(e)}"
        )
        raise
    logger.info(
        f"Updated current balance for {'vendor' if is_vendor_credit else 'customer'} "
        f"ID: {new_transaction.vendor.id if is_vendor_credit else new_transaction.customer.id} "
        f"with transaction ID: {new_transaction.id}"
    )
