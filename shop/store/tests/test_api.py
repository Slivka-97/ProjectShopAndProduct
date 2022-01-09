import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Product
from products.serializers import ProductSerializer


class ShopApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user")
        self.prod1 = Product.objects.create(name="Meat1", weight=500, supplier='supplier1')
        self.prod2 = Product.objects.create(name="Meat2", weight=1500, supplier='supplier2')
        self.prod3 = Product.objects.create(name="Meat3", weight=2500, supplier='supplier3')
        self.prod4 = Product.objects.create(name="Meat4", weight=1500, supplier='supplier3', owner=self.user)

    def test_get(self):
        url = reverse("product-list")
        response = self.client.get(url)
        serializer_data = ProductSerializer([self.prod1, self.prod2, self.prod3, self.prod4], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse("product-list")
        response = self.client.get(url, data={'weight': 1500})
        serializer_data_filter = ProductSerializer([self.prod2, self.prod4], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data_filter, response.data)

    def test_get_search(self):
        url = reverse("product-list")
        response = self.client.get(url, data={'search': 'supplier3'})
        serializer_data_search = ProductSerializer([self.prod3, self.prod4], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data_search, response.data)

    def test_get_ordering(self):
        url = reverse("product-list")
        response = self.client.get(url, data={'ordering': '-weight'})
        serializer_data_order = ProductSerializer([self.prod3, self.prod2, self.prod4, self.prod1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data_order, response.data)

    def test_post(self):
        url = reverse("product-list")
        data = {
            "name": "Chocolat",
            "weight": "250",
            "supplier": "ChocolatFactory"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.user, Product.objects.last().owner)

    def test_put(self):
        url = reverse("product-detail", args=(self.prod4.id,))
        data = {
            "name": "Chocolat",
            "weight": 255,
            "supplier": "ChocolatFactory"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.prod4.refresh_from_db()
        self.assertEqual(255, self.prod4.weight)

    def test_get_one_product(self):
        url = reverse("product-detail", args=(self.prod1.id,))
        data = {
            "id": 1,
            "name": "Meat1",
            "weight": "500.00",
            "supplier": "supplier1"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data.get('name'), response.data.get('name'))

    def test_update_no_owner_but_staff(self):
        user2 = User.objects.create(username="user1", is_staff=True)
        url = reverse("product-detail", args=(self.prod4.id,))
        data = {
            "name": "Meat4",
            "weight": 100,
            "supplier": "supplier4"
        }
        json_data = json.dumps(data)
        self.client.force_login(user2)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.prod4.refresh_from_db()
        self.assertEqual(100, self.prod4.weight)


class ProductRelationApiTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="test_user1")
        self.user2 = User.objects.create_user(username="test_user2")
        self.prod1 = Product.objects.create(name="Meat1", weight=500, supplier='supplier1')
        self.prod2 = Product.objects.create(name="Meat2", weight=1500, supplier='supplier2')
        self.prod3 = Product.objects.create(name="Meat3", weight=2500, supplier='supplier3')
        self.prod4 = Product.objects.create(name="Meat4", weight=1500, supplier='supplier3', owner=self.user1)

    def test_like(self):
        url = reverse("userproductrelation-detail", args=(self.prod4.id,))

        data = {
            "like": True
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.prod1.refresh_from_db()
        print(self.prod4)
        self.assertTrue(self.prod4.like)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
