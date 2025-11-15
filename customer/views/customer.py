from rest_framework.decorators import api_view
from rest_framework.response import Response

from customer.services import CustomerService
from customer.serializers import IncreaseCustomerCreditSerializer


@api_view(["POST"])
def increase_credit(request):
    serializer = IncreaseCustomerCreditSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        CustomerService.increase_credit(**serializer.validated_data)
    except ValueError as e:
        return Response({"message": str(e)}, status=400)

    return Response({"data": serializer.data})
