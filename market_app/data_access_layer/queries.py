from market_app.models import Client, Purchase, Product


def get_all_client():
    return Client.objects.all()


def get_all_product():
    return Product.objects.all()


def get_all_purchase():
    return Purchase.objects.all()


def get_client_by_id(client_id):
    return Client.objects.filter(pk=client_id).first()


def get_product_by_id(product_id):
    return Product.objects.filter(pk=product_id).first()


def get_purchase_by_id(purchase_id):
    return Purchase.objects.filter(pk=purchase_id).first()


def create_purchase(data):
    return Purchase.objects.create(client=data['client'], product=data['product'])


def get_full_purchase(client_id):
    return Purchase.objects.filter(client=client_id).select_related('product')
