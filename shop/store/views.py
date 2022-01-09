from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from store.models import Shop
from store.serializers import ShopSerializer


def index(requests):
    return render(requests, "index.html", {'product': Shop.objects.all()})


def auth(requests):
    return render(requests, 'oauth.html')


class ShopView(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
