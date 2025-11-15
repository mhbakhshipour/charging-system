from charging_system_b2b.utils.views import BaseModelViewSet

from vendor.models import Vendor
from vendor.serializers import VendorSerializer


class VendorViewSet(BaseModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    search_fields = ["name"]
    permission_classes = []

    def perform_create(self, serializer):
        serializer.save()
