from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from market_app.data_access_layer.queries import get_all_product, get_product_by_id
from market_app.documents import ProductDocument
from market_app.serializers import ProductSerializer
from market_app.views.paginated_elastic_search import PaginatedElasticSearchView
from django.forms.models import model_to_dict
from elasticsearch_dsl import Q


class ProductViewSet(viewsets.ViewSet):
    queryset = get_all_product()

    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='get_product')
    def get_product(self, request):
        pk = request.query_params.get('pk', None)
        product = get_product_by_id(pk)
        serializer = ProductSerializer(data=model_to_dict(product))
        if not serializer.is_valid():
            return Response({'error': serializer.errors})
        return Response(serializer.data)


class ProductSearchView(PaginatedElasticSearchView):
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
        serializer_data = self.get_response_or_error(query)
        return serializer_data
