from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from market_app.models import Product


@registry.register_document
class ProductDocument(Document):
    class Index:
        name = 'product_index'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
        ]

