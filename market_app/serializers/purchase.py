from datetime import timezone

from rest_framework import serializers

from ..data_access_layer.queries import get_all_client, get_all_product
from ..models import Purchase, Client, Product


class PurchaseSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    client = serializers.PrimaryKeyRelatedField(queryset=get_all_client())
    product = serializers.PrimaryKeyRelatedField(queryset=get_all_product())

    class Meta:
        model = Purchase
        fields = ['id', 'client', 'product']
        read_only_fields = ['id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['client'] = instance.client.name
        representation['product'] = instance.product.name
        return representation
