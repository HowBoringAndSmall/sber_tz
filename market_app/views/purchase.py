from django.forms import model_to_dict
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from market_app.data_access_layer.queries import get_all_purchase, create_purchase, get_full_purchase, \
    get_purchase_by_id
from market_app.serializers import PurchaseSerializer


class PurchaseViewSet(viewsets.ViewSet):
    queryset = get_all_purchase()

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
        pk = request.query_params.get('pk', None)
        purchases = get_purchase_by_id(pk)
        serializer = PurchaseSerializer(data=model_to_dict(purchases))
        if not serializer.is_valid():
            return Response({'error': serializer.errors})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='client_purchase_with_product')
    def client_purchase_with_product(self, request):
        client_id = self.request.query_params.get('client', None)
        purchases = get_full_purchase(client_id)
        if not purchases:
            return Response({'error': f'No purchases found for client with id {client_id}'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = PurchaseSerializer(purchases, many=True)
        return Response(serializer.data)






