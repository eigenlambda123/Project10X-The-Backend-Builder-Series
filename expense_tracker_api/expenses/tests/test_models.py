from django.test import TestCase
from django.contrib.auth.models import User
from expenses.models import Category, Transactions
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

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


class TransactionsModelTests(TestCase):
    """
    """
    def setUp(self):
        self.user = User.objects.create_user(username='rmvilla', password='password') # create new user
        self.category = Category.objects.create(name='Bills', user=self.user) # create new category with user set to self.user


    def test_create_transaction_valid(self):
        """
        Test that a valid Transactions object can be created with the required fields,
        and that its attributes are correctly set upon creation.
        """

        # create new transaction
        transaction = Transactions.objects.create(
            user=self.user,
            category=self.category,
            title='Electricity Bill',
            description='Monthly bill',
            type='expense',
            amount=100.00
        )
        self.assertEqual(transaction.title, 'Electricity Bill') # check if transaction title is correct
        self.assertEqual(transaction.type, 'expense') # check if transaction type is correct
        self.assertEqual(transaction.amount, 100.00) # check if transaction amount is correct
        self.assertEqual(transaction.category, self.category) # check if transaction category is correct
        self.assertEqual(transaction.user, self.user) # check if user of the transaction is set properly


    def test_invalid_transaction_type_raises(self):
        """
        Test that creating a Transactions instance with an invalid 'type' value raises a ValidationError.

        This test ensures that the 'type' field in the Transactions model only accepts valid choices.
        If an invalid value is provided, calling full_clean() should raise a ValidationError.
        """

        # create new transacction
        transaction = Transactions(
            user=self.user,
            category=self.category,
            title='Unknown',
            type='invalid_type',
            amount=50
        )
        with self.assertRaises(ValidationError):
            transaction.full_clean()  # Should raise due to invalid choice

    
    def test_amount_decimal_places(self):
        """
        Test that the Transactions model enforces a maximum of two decimal places for the 'amount' field.
        Attempts to create a transaction with more than two decimal places should raise a ValidationError.
        """
        transaction = Transactions(
            user=self.user,
            category=self.category,
            title='Partial Payment',
            type='income',
            amount=123.4567  # More than 2 decimal places
        )
        with self.assertRaises(ValidationError):
            transaction.full_clean()

