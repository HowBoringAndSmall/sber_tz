from ..models import Client, Product, Purchase


def get_client_by_id(client_id):
    return Client.objects.get(pk=client_id)


def get_product_by_id(product_id):
    return Product.objects.get(pk=product_id)


def create_purchase(data):
    return Purchase.objects.create(client=data['client'], product=data['product'])
