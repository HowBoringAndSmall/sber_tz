from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from .data_access_layer.queries import create_purchase
from .models import Client, Product, Purchase
from .serializers.client import ClientSerializer
from .serializers.product import ProductSerializer
from .serializers.purchase import PurchaseSerializer


class ProductViewSet(viewsets.ViewSet):
    queryset = Product.objects.all()

    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        # if not serializer.is_valid():
        #     return Response({'error': 'Invalid data'})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='get_product')
    def get_product(self, request):
        pk = self.request.query_params.get('pk', None)
        product = get_object_or_404(self.queryset, pk=pk)
        serializer = ProductSerializer(product)
        if not serializer.is_valid():
            return Response({'error': 'Invalid data'})
        return Response(serializer.data)


class PurchaseViewSet(viewsets.ViewSet):
    queryset = Purchase.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = PurchaseSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        new_purchase = create_purchase(serializer.validated_data)
        return Response(PurchaseSerializer(new_purchase).data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        serializer = PurchaseSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='get_purchase')
    def get_purchase(self, request):
        pk = self.request.query_params.get('pk', None)
        purchases = get_object_or_404(self.queryset, pk=pk)
        serializer = PurchaseSerializer(data=purchases)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='client_purchase_with_product')
    def client_purchase_with_product(self, request):
        client_id = self.request.query_params.get('client', None)
        purchases = Purchase.objects.filter(client=client_id).select_related('product')
        if not purchases:
            return Response({'error': f'No purchases found for client with id {client_id}'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = PurchaseSerializer(purchases, many=True)
        return Response(serializer.data)

