from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from expenses.models import Category, Transactions

class AuthPermissionTests(APITestCase):
    def authenticate(self):
        """
        defined for getting a token via given user
        """
        self.user = User.objects.create_user(username='authuser', password='testpass123')
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'authuser', 'password': 'testpass123'})
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')


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


    def test_authorized_access_returns_200(self):
        """
        Test that an authenticated user can access the category and transaction endpoints
        """
        self.authenticate()  # Authenticate the test client with a valid JWT token

        category_url = reverse('category-list')  # URL for the category-list endpoint
        expense_url = reverse('transactions-list')  # URL for the transactions-list endpoint

        # Send GET requests to both endpoints as an authenticated user
        response1 = self.client.get(category_url)
        response2 = self.client.get(expense_url)

        # Assert that both endpoints return HTTP 200 OK for authenticated access
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)


    def test_user_sees_only_their_own_data(self):
        """
        Test for confirming that user can only see their own data
        """
        # Create two users
        user1 = User.objects.create_user(username='user1', password='pass1234')
        user2 = User.objects.create_user(username='user2', password='pass5678')

        # Create categories and expenses for both
        cat1 = Category.objects.create(name='Food', user=user1)
        cat2 = Category.objects.create(name='Bills', user=user2)

        Transactions.objects.create(title='Lunch', amount=12, type='expense', category=cat1, user=user1)
        Transactions.objects.create(title='Electricity', amount=50, type='expense', category=cat2, user=user2)

        # Authenticate as user1
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'user1', 'password': 'pass1234'})
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # GET categories and expenses
        category_url = reverse('category-list')
        expense_url = reverse('transactions-list')

        cat_response = self.client.get(category_url)
        exp_response = self.client.get(expense_url)

        self.assertEqual(cat_response.status_code, status.HTTP_200_OK)
        self.assertEqual(exp_response.status_code, status.HTTP_200_OK)

        # Only one category and one expense should be visible to user1
        self.assertEqual(len(cat_response.data), 1)
        self.assertEqual(cat_response.data[0]['name'], 'Food')

        self.assertEqual(len(exp_response.data), 1)
        self.assertEqual(exp_response.data[0]['title'], 'Lunch')



