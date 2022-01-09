from rest_framework.serializers import ModelSerializer

from products.models import UserProductRelation
from store.models import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class UserProductRelationSerializer(ModelSerializer):
    class Meta:
        model = UserProductRelation
        fields = ('product', 'like', 'in_basket', 'rate')
