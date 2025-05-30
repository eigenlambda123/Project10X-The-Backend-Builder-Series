from django.test import TestCase
from django.contrib.auth.models import User
from blog_app.models import Post, Category, Tag
from blog_app.serializers import PostSerializer

class PostSerializerTest(TestCase):
    """
    Test case for the PostSerializer.
    """

    def setUp(self):
        """
        Set up the test environment by creating a user, category, and tag.
        """
        self.user = User.objects.create_user(username="testuser", password="secret123") # Create a test user
         # This user will be used as the author of the post
        self.category = Category.objects.create(name="Django") # Create a test category
        self.tag1 = Tag.objects.create(name="testing") # Create a test tag

        # Create a dictionary with valid data for the serializer
        self.valid_data = { 
            "title": "Test Post",
            "content": "This is a test post content.",
            "author": self.user.id,
            "category": self.category.name,
            "tags": [self.tag1.name]
        }

    def test_serializer_with_valid_data(self):
        serializer = PostSerializer(data=self.valid_data) # Initialize the serializer with valid data
        is_valid = serializer.is_valid() # Check if the serializer is valid
        print("Errors:", serializer.errors)  # Print any validation errors for debugging
        self.assertTrue(is_valid) # Ensure the serializer is valid
        self.assertEqual(serializer.validated_data['title'], "Test Post") # Check if the title is correctly validated


    
    def test_missing_title_fails(self):
        invalid_data = self.valid_data.copy() # Create a copy of the valid data
        invalid_data.pop('title') # Remove the title to make it invalid
        serializer = PostSerializer(data=invalid_data) # Initialize the serializer with invalid data
        self.assertFalse(serializer.is_valid()) # Check if the serializer is invalid
        self.assertIn('title', serializer.errors) # Ensure the error is related to the title field


    def test_title_too_long_fails(self):
        invalid_data = self.valid_data.copy() # Create a copy of the valid data
        invalid_data["title"] = "a" * 300  # Create a title that exceeds the maximum length
        serializer = PostSerializer(data=invalid_data) # Initialize the serializer with invalid data
        self.assertFalse(serializer.is_valid()) # Check if the serializer is invalid
        self.assertIn('title', serializer.errors) # Ensure the error is related to the title field

    
