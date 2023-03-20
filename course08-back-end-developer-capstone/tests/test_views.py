from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from Restaurant.models import MenuItem
from Restaurant.serializers import MenuItemSerializer
from Restaurant.views import MenuItemsView


class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.menuitem1 = MenuItem.objects.create(title='Pizza', price=12.99, featured=True, category_id=1)
        self.menuitem2 = MenuItem.objects.create(title='Burger', price=8.99, featured=False, category_id=2)
        self.menuitem3 = MenuItem.objects.create(title='Fries', price=3.99, featured=True, category_id=2)

    def test_getall(self):
        response = self.client.get('/menu/')
        menuitems = MenuItem.objects.all()
        serializer = MenuItemSerializer(menuitems, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

