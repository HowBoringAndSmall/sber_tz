from rest_framework import serializers
from .models import Client, Product, Purchase


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'email']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class PurchaseSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    product = ProductSerializer()

    class Meta:
        model = Purchase
        fields = ['id', 'client', 'product', 'purchase_date']
