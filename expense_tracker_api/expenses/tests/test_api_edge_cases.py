from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from expenses.models import Category, Transactions


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


    def test_create_transaction_missing_required_fields(self):
        """
        Test that Should return 400 if required fields are missing
        """
        url = reverse('transactions-list') # transactions-list endpoint

        # dummy input data with missing fields
        data = {
            'title': '',  # Missing
            'amount': '',  # Missing
            'type': 'expense',
            'category': self.cat1.id
        }

        response = self.client.post(url, data) # send a post request to transactions-list endpoint
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # check if status 400 bad request
        self.assertIn('title', response.data) # check if  the error involved the title
        self.assertIn('amount', response.data) # check if  the error involved the amount


    def test_create_transaction_invalid_category(self):
        """
        Test that Should return 400 if the category ID does not exist or does not belong to user
        """
        url = reverse('transactions-list') # transactions-list endpoint
        invalid_category_id = 999  # id that Doesn't exist
        data = {
            'title': 'Test',
            'amount': 10,
            'type': 'expense',
            'category': invalid_category_id # invalid id
        }

        response = self.client.post(url, data) # send a post request to transactions-list endpoint
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # check if status 400 bad request
        self.assertIn('category', response.data) # check if  the error involved the category

    def test_create_transaction_negative_amount(self):
        """
        Test that Should reject negative amounts if not allowed
        """

        url = reverse('transactions-list') # transactions-list endpoint
        data = {
            'title': 'Bad Expense',
            'amount': -50, # negative ammount
            'type': 'expense',
            'category': self.cat1.id
        }

        response = self.client.post(url, data) # send a post request to transactions-list endpoint
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # check if status 400 bad request
        self.assertIn('amount', response.data) # check if  the error involved the amount


    def test_user_cannot_update_another_users_transaction(self):
        """
        Test that an authenticated user cannot update another user's transaction
        """

        # Create a transaction belonging to user2
        other_tx = Transactions.objects.create(
            title='Other Expense',
            amount=30,
            type='expense',
            category=self.cat2,
            user=self.user2
        )

        url = reverse('transactions-detail', args=[other_tx.id])  # Get the detail endpoint for the transaction
        data = {'title': 'Hacked!', 'amount': 999}  # Attempt to update with new data

        response = self.client.put(url, data)  # Send a PUT request as user1
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Should return 404 Not Found


    def test_user_cannot_delete_another_users_transaction(self):
        """
        Test that an authenticated user cannot delete another user's transaction
        """
        # Create a transaction that belongs to user2
        other_tx = Transactions.objects.create(
            title='Other Expense',
            amount=30,
            type='expense',
            category=self.cat2,
            user=self.user2
        )

        url = reverse('transactions-detail', args=[other_tx.id])  # Get the detail endpoint for the transaction
        response = self.client.delete(url)  # Attempt to delete as user1 (authenticated)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Should return 404 Not Found