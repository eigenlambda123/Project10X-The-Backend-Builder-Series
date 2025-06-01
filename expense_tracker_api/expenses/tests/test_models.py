from django.test import TestCase
from django.contrib.auth.models import User
from expenses.models import Category
from django.db.utils import IntegrityError

class CategoryModelTests(TestCase):
    """
    Tests for the Category model, including slug generation,
    custom slug preservation, string representation, and unique constraints.
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

    def test_slug_not_overwritten_if_exists(self):
        """
        Test that if a Category is created with a custom slug,
        saving the object does not overwrite the provided slug
        with an auto-generated one.
        """
        category = Category(name='Utilities', user=self.user, slug='custom-slug') # create a new Category with custom slug
        category.save() # save 
        self.assertEqual(category.slug, 'custom-slug') # check if the custom slug isnt overwritten

    def test_unique_together_name_user(self):
        Category.objects.create(name='Travel', user=self.user) # create new category
        with self.assertRaises(IntegrityError):
            # Creating a category with same name and user should raise error
            Category.objects.create(name='Travel', user=self.user)