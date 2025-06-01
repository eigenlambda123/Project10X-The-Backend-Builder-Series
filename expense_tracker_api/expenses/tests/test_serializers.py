from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from expenses.models import Category, Transactions
from expenses.serializers import CategorySerializer, TransactionsSerializer

class CategorySerializerTest(TestCase):
    """
    """
    def setUp(self):
        """
        Set up test dependencies before each test method.

        Initializes a RequestFactory instance for simulating HTTP requests in tests.
        Creates a test user for authentication-related test cases.
        """
        self.factory = RequestFactory() 
        self.user = User.objects.create_user(username='testuser', password='pass') # create test user
