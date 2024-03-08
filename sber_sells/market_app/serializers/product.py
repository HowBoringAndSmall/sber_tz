from rest_framework import serializers
from ..models import Purchase, Client, Product


class ProductSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(max_length=500, allow_null=True, allow_blank=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price']
