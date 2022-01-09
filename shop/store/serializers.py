from rest_framework.serializers import ModelSerializer

from store.models import Shop


class ShopSerializer(ModelSerializer):
    class Meta:
        model = Shop
        fields = ['product', 'price']
