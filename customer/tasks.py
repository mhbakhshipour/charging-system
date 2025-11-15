from celery.utils.log import get_task_logger
from redlock import RedLock

from charging_system_b2b.celery import app
from charging_system_b2b.settings import CELERY_BROKER_URL

from vendor.models import Vendor
from customer.models import Customer
from customer.services import CustomerService


logger = get_task_logger(__name__)


@app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 10, "countdown": 5})
def increase_customer_credit_task(self, vendor_id: int, customer_id: int, amount: int):
    dlm = RedLock(
        f"increase_customer_credit:{vendor_id}:{customer_id}",
        connection_details=[{"url": CELERY_BROKER_URL}],
    )
    lock = dlm.acquire()
    if not lock:
        return
    try:
        vendor = Vendor.objects.get(id=vendor_id)
        customer = Customer.objects.get(id=customer_id)
        CustomerService.increase_credit(vendor=vendor, amount=amount, customer=customer)
    finally:
        dlm.release()