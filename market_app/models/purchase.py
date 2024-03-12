from django.db import models


class Purchase(models.Model):
    client = models.ForeignKey('market_app.Client', on_delete=models.CASCADE)
    product = models.ForeignKey('market_app.Product', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.client.name} bought {self.product.name}"
