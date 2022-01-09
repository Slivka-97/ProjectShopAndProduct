from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class Shop(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
