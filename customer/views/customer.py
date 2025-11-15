from charging_system_b2b.utils.views import BaseModelViewSet

from customer.models import Customer
from customer.serializers import CustomerSerializer


class CustomerViewSet(BaseModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    search_fields = ["phone_number"]
    permission_classes = []

    def perform_create(self, serializer):
        serializer.save()
