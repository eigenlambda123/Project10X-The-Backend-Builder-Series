from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from expenses.models import Category,  Transactions
from django.urls import reverse
from rest_framework import status

class CategoryAPITest(APITestCase):
    """
    API tests for the Category endpoints.

    These tests verify:
    - Categories can be created via the API.
    - The category list endpoint returns the correct data.
    - Authentication is required for category actions.
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

    def test_list_categories(self):
        """
        Test that the category_url is returning properly
        """

        # Create dummy category data
        Category.objects.create(name='Groceries', user=self.user)
        Category.objects.create(name='Transport', user=self.user)

        response = self.client.get(self.category_url) # send a GET request in category_url
        self.assertEqual(response.status_code, status.HTTP_200_OK) # check if status 200 ok
        self.assertEqual(len(response.data), 2) # check if the length of retured data is 2


class TransactionAPITest(APITestCase):
    """
    API tests for the Transactions endpoints.

    These tests verify:
    - Transactions can be created, listed, updated, and deleted via the API.
    - The correct status codes and data are returned for each operation.
    - Authentication is required for transaction actions.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='john', password='pass1234') # create dummy user
        self.client = APIClient() # use for Actualt Endpoints
        self.client.force_authenticate(user=self.user) # bypass authentication
        self.category = Category.objects.create(name='Bills', user=self.user) # created new category

        self.transaction_url = reverse('transactions-list')  # http://127.0.0.1:8000/api/transactions/ endpoint 


    def test_create_transaction(self):
        """
        Test that a transaction can be successfully created via the API
        """

        # Input data for the new transaction
        data = {
            'title': 'Electric Bill',
            'description': 'Monthly payment',
            'type': 'expense',
            'amount': '50.00',
            'category': self.category.id
        }
        response = self.client.post(self.transaction_url, data)  # Send POST request to transaction_url with data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Check if status is 201 Created
        self.assertEqual(response.data['title'], 'Electric Bill')  # Check if the created transaction's title is correct
        self.assertEqual(response.data['amount'], '50.00')  # Check if the amount is correct

    
    def test_get_transaction_list(self):
        """
        Test if accessing transaction-list endpoint is working
        """
        # create new transactions
        Transactions.objects.create(
            user=self.user, category=self.category,
            title='Water Bill', type='expense', amount=30
        )
        Transactions.objects.create(
            user=self.user, category=self.category,
            title='Internet', type='expense', amount=45
        )

        response = self.client.get(self.transaction_url) # navigate to transaction-list 
        self.assertEqual(response.status_code, status.HTTP_200_OK) # check if status 200 ok
        self.assertEqual(len(response.data), 2) # check if the length of transaction-list == 2

    def test_update_transaction(self):
        """
        Test if accessing transaction endpoint and updating a transaction is working
        """

        # dummy created existing transaction
        txn = Transactions.objects.create(
            user=self.user, category=self.category,
            title='Phone Bill', type='expense', amount=60
        )
        url = reverse('transactions-detail', kwargs={'pk': txn.pk}) # navigate to transaction-list -> detail post using txn as pk

        updated_data = {'title': 'Updated Phone Bill', 'amount': '70.00', 'type': 'expense', 'category': self.category.id} # input data for updating 
        response = self.client.put(url, updated_data) # update the url using the updated_data

        self.assertEqual(response.status_code, status.HTTP_200_OK) # check if status 200 ok
        self.assertEqual(response.data['title'], 'Updated Phone Bill') # check if title is properly updated
        self.assertEqual(response.data['amount'], '70.00') # check if amount is properly updated


    def test_delete_transaction(self):
        """
        Test if accessing transaction endpoint and deleting a transaction is working
        """

        # dummy created existing transaction
        txn = Transactions.objects.create(
            user=self.user, category=self.category,
            title='Gas Bill', type='expense', amount=40
        )
        url = reverse('transactions-detail', kwargs={'pk': txn.pk}) # navigate to transaction-list -> detail post using txn as pk
        response = self.client.delete(url) # delete the exisiting txn data accessing the url endpoint
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) # check if status 204 no content
        self.assertFalse(Transactions.objects.filter(pk=txn.pk).exists()) # check if txn doesnt exist anymore


    
