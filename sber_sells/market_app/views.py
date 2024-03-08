from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from .models import Client, Product, Purchase
from .serializers import ClientSerializer, ProductSerializer, PurchaseSerializer


class ProductViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def list_products(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        # if not serializer.is_valid():
        #     return Response({'error': 'Invalid data'})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def retrieve_product(self, request, pk=None):
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        serializer = ProductSerializer(product)
        # if not serializer.is_valid():
        #     return Response({'error': 'Invalid data'})
        return Response(serializer.data)


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    @action(detail=True, methods=['post'])
    def create_purchase(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)

        client = request.user

        purchase = Purchase.objects.create(product=product, client=client)
        serializer = PurchaseSerializer(purchase)
        # if not serializer.is_valid():
        #     return Response({'error': 'Invalid data'})
        return Response(serializer.data)