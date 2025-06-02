from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class AuthPermissionTests(APITestCase):
    def test_user_can_register_successfully(self):
        url = reverse('register') # access register url endpoint

        # input data
        data = {
            'username': 'testuser',
            'email': 'testemail@gmail.com',
            'password': 'strongpassword123'
        }

        response = self.client.post(url, data) # access register with APICLient and post the data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # check if status 201 created
        self.assertTrue(User.objects.filter(username='testuser').exists()) # check if the user is created successfully


    def test_user_can_obtain_jwt_token(self):
        """
        Test that a user can obtain a JWT token using valid credentials.
        """
        User.objects.create_user(username='testuser', password='strongpassword123')  # Create a new user
        url = reverse('token_obtain_pair')  # Get the URL for the JWT token endpoint

        # Input user credentials
        data = {
            'username': 'testuser',
            'password': 'strongpassword123'
        }

        response = self.client.post(url, data)  # Send POST request to obtain JWT token
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Check for 200 OK status
        self.assertIn('access', response.data)  # Check if access token is present in the response
        self.assertIn('refresh', response.data)  # Check if refresh token is present in the response


    def test_unauthorized_access_returns_401(self):
        """
        Test if unauthorized user cannot access category and transaction endpoints
        """
        category_url = reverse('category-list')
        expense_url = reverse('transactions-list')

        response1 = self.client.get(category_url)
        response2 = self.client.get(expense_url)

        self.assertEqual(response1.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)

