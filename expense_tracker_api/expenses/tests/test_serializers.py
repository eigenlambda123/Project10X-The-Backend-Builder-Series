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

    def get_serializer_context(self):
        """
        Returns serializer context with a mock request and test user.
        """
        request = self.factory.get('/') # Create a mock GET request to the root URL
        request.user = self.user # Assign the test user to the request
        return {'request': request} # Return context dictionary with the request
    
    def test_valid_data_creates_category(self):
        """
        Test if creating a Category with valid data is working correctly
        """

        data = {'name': 'Food'}  # Input data for the Category
        serializer = CategorySerializer(data=data, context=self.get_serializer_context())  # Initialize serializer with data and context
        self.assertTrue(serializer.is_valid(), serializer.errors)  # Assert that the serializer validates the input data
        category = serializer.save()  # Save the validated data and create a Category instance
        self.assertEqual(category.name, 'Food')  # Assert the category name is set correctly
        self.assertEqual(category.user, self.user)  # Assert the category user is set to the test user

