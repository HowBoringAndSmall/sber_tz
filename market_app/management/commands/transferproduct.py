from django.core.management.base import BaseCommand
from django.forms import model_to_dict
from elasticsearch_dsl import connections
from market_app.data_access_layer.queries import get_all_product
from market_app.documents import ProductDocument


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        connections.create_connection(hosts=['elasticsearch'])

        queryset = get_all_product()

        for obj in queryset:
            doc = ProductDocument(model_to_dict(obj))
            doc.save()
