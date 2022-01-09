from django.contrib import admin
from django.contrib.admin import ModelAdmin

from products.models import Product, UserProductRelation


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    pass


@admin.register(UserProductRelation)
class UserProductRelationAdmin(ModelAdmin):
    pass
