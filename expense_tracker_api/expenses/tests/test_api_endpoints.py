from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from expenses.models import Category
from django.urls import reverse
from rest_framework import status

class CategoryAPITest(APITestCase):
    """
    """
    def setUp(self):
        self.user = User.objects.create_user(username='john', password='pass1234') # create dummy user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user) # bypass authentication
        self.category_url = reverse('category-list')  # if using DRF ViewSets with routers


    def test_create_category(self):
        """
        Test that a category can be successfully created via the API
        """
        data = {'name': 'Food'} # input data
        response = self.client.post(self.category_url, data) # send post request to category_url using data as context
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # check if status 201 created
        self.assertEqual(response.data['name'], 'Food') # check if the created data exist
        self.assertIn('slug', response.data) # check if slug is also created 
