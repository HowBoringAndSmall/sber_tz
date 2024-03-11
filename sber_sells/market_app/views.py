import abc

from rest_framework import viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from .data_access_layer.queries import create_purchase, get_all_purchase, get_all_product, get_full_purchase
from .documents import ProductDocument
# from django_elasticsearch_dsl.viewsets import DocumentViewSet
from .models import Client, Product, Purchase
from .serializers.client import ClientSerializer
from .serializers.product import ProductSerializer
from .serializers.purchase import PurchaseSerializer
from elasticsearch_dsl import Q
from django_elasticsearch_dsl.search import Search


class ProductViewSet(viewsets.ViewSet):
    queryset = get_all_product()

    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
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
        pk = self.request.query_params.get('pk', None)
        purchases = get_object_or_404(self.queryset, pk=pk)
        serializer = PurchaseSerializer(data=purchases)
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


class PaginatedElasticSearchAPIView(viewsets.ViewSet, LimitOffsetPagination):
    serializer_class = None
    document_class = None

    @abc.abstractmethod
    def generate_q_expression(self, query):
        """This method should be overridden
        and return a Q() expression."""

    def get_response_or_error(self, request, query):
        try:
            q = self.generate_q_expression(query)
            search = self.document_class.search().query(q)
            response = search.execute()
            if not response.hits:
                return Response({'message': 'No products found for the given query'}, status=status.HTTP_200_OK)

            serializer = self.serializer_class(response.hits, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductSearch(PaginatedElasticSearchAPIView):
    serializer_class = ProductSerializer
    document_class = ProductDocument

    def generate_q_expression(self, query):
        queries = []
        name = query.get('name', None)
        description = query.get('description', None)
        price = query.get('price', None)
        if name:
            queries.append(Q('match', name=name))

        if description:
            queries.append(Q('match', description=description))

        if price:
            queries.append(Q('match', price=price))

        if queries:
            return Q('bool', should=queries, minimum_should_match=1)
        else:
            return Q()

    @action(detail=False, methods=['get'], url_path='get_product')
    def get_search_product(self, request):
        query = {
            'name': request.query_params.get('name'),
            'description': request.query_params.get('description'),
            'price': request.query_params.get('price'),
        }
        serializer_data = self.get_response_or_error(request, query)
        return serializer_data

