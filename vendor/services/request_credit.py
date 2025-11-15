from django.db import transaction

from vendor.models import RequestCredit
from vendor.services.vendor import VendorCreditService


class RequestCreditService:

    @staticmethod
    @transaction.atomic
    def confirm_request_credit(request_credit: RequestCredit):
        request_credit = request_credit.__class__.objects.select_for_update().get(
            pk=request_credit.id
        )

        if request_credit.status == RequestCredit.RequestCreditStatus.CONFIRMED:
            return request_credit

        VendorCreditService.increase_credit(
            request_credit.requester, request_credit.amount
        )

        request_credit.status = RequestCredit.RequestCreditStatus.CONFIRMED
        request_credit.save(update_fields=["status"])

        return request_credit
