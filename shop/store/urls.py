from django.urls import path, include
from rest_framework.routers import SimpleRouter

from products.views import ProductView, UserProductRelationView
from .views import *

router = SimpleRouter()
router.register('shop', ShopView)
router.register('product', ProductView)
router.register('product_relation', UserProductRelationView)

urlpatterns = [
    path('auth/', auth),
    path('', include('social_django.urls', namespace='social'))
]
urlpatterns += router.urls
