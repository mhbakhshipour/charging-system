from charging_system_b2b.utils.serializers.base_model_serializer import (
    BaseModelserializer,
)

from customer.models.customer import Customer


class CustomerSerializer(BaseModelserializer):
    class Meta:
        model = Customer
        fields = ["phone_number", "created_at", "updated_at"]
