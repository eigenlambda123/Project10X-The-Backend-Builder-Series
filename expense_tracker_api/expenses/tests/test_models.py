from django.test import TestCase
from django.contrib.auth.models import User
from expenses.models import Category

class CategoryModelTests(TestCase):
    """
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password') # create dummy user

    
    def test_create_category_and_slug_generation(self):
        """
        Test that creating a Category automatically generates the correct slug
        and that the string representation returns the category name.
        """
        category = Category.objects.create(name='Groceries', user=self.user)  # create new category
        self.assertEqual(category.name, 'Groceries')  # check if the category name is correct
        self.assertEqual(category.slug, 'groceries')  # check if slug is auto-generated correctly
        self.assertEqual(str(category), 'Groceries')  # check string representation of category