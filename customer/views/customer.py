from rest_framework.decorators import api_view
from rest_framework.response import Response

from customer.serializers import IncreaseCustomerCreditSerializer
from customer.tasks import increase_customer_credit_task


@api_view(["POST"])
def increase_credit(request):
    serializer = IncreaseCustomerCreditSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    vendor = serializer.validated_data["vendor"]
    customer = serializer.validated_data["customer"]
    amount = serializer.validated_data["amount"]
    increase_customer_credit_task.delay(vendor.id, customer.id, amount)
    return Response({"status": "accepted", "data": serializer.data}, status=202)
