from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from expenses.models import Category


class TransactionEdgeCaseTests(APITestCase):
    """
    """
    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass456')

        # Create categories for each user
        self.cat1 = Category.objects.create(name='Food', user=self.user1)
        self.cat2 = Category.objects.create(name='Utilities', user=self.user2)

        # Authenticate as user1
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'user1', 'password': 'pass123'})
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')