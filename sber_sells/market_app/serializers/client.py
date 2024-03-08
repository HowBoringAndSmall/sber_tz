from rest_framework import serializers
from ..models import Purchase, Client, Product


class ClientSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'name', 'email']
