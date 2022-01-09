from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=7, decimal_places=2)
    supplier = models.CharField(max_length=250)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                              related_name='my_product')
    views = models.ManyToManyField(User, through='UserProductRelation',
                                   related_name='products')

    def __str__(self):
        return self.name


class UserProductRelation(models.Model):
    RATE_CHOICES = (
        (1, 'terrible'),
        (2, 'bad'),
        (3, 'normal'),
        (4, 'god'),
        (5, 'fine')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_basket = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)

    def __str__(self):
        return f"{self.user} : {self.product}"
