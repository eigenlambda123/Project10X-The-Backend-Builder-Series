from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from expenses.models import Category
from django.urls import reverse

class CategoryAPITest(APITestCase):
    """
    """
    def setUp(self):
        self.user = User.objects.create_user(username='john', password='pass1234') # create dummy user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user) # bypass authentication
        self.category_url = reverse('category-list')  # if using DRF ViewSets with routers
