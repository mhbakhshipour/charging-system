from charging_system_b2b.utils.serializers.base_model_serializer import (
    BaseModelserializer,
)

from transaction.models import Transaction
from transaction.services import TransactionService


class TransactionSerializer(BaseModelserializer):
    class Meta:
        model = Transaction
        fields = ["vendor", "customer", "amount", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        return TransactionService.add_transaction(**validated_data)
