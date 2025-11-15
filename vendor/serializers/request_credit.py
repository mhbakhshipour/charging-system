from charging_system_b2b.utils.serializers.base_model_serializer import (
    BaseModelserializer,
)

from vendor.models.request_credit import RequestCredit


class RequestCreditSerializer(BaseModelserializer):
    class Meta:
        model = RequestCredit
        fields = ["requester", "amount", "status", "created_at", "updated_at"]
        read_only_fields = ["status", "created_at", "updated_at"]
