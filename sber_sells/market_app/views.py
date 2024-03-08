from rest_framework import viewsets, status
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


class PurchaseViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        data = request.data

        try:
            client = Client.objects.get(pk=data.get('client'))
            product = Product.objects.get(pk=data.get('product'))
            new_purchase = Purchase.objects.create(
                client=client,
                product=product,
            )

            serializer = PurchaseSerializer(new_purchase)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        purchases = Purchase.objects.all()
        serializer = PurchaseSerializer(purchases, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def client_purchase(self, request, client_id=None):
        purchases = Purchase.objects.filter(client=client_id)
        serializer = PurchaseSerializer(purchases, many=True)
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

