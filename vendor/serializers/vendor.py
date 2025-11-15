from charging_system_b2b.utils.serializers.base_model_serializer import (
    BaseModelserializer,
)

from vendor.models.vendor import Vendor


class VendorSerializer(BaseModelserializer):
    class Meta:
        model = Vendor
        fields = ["name", "created_at", "updated_at"]
