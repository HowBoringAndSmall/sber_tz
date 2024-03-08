from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    client = models.ForeignKey('market_app.Client', on_delete=models.CASCADE)
    product = models.ForeignKey('market_app.Product', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.client.name} bought {self.product.name}"
