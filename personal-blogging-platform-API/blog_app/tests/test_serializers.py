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
            "category": self.category.id,
            "tags": [self.tag1.id]
        }

    def test_serializer_with_valid_data(self):
        serializer = PostSerializer(data=self.valid_data) # Initialize the serializer with valid data
        self.assertTrue(serializer.is_valid()) #     Check if the serializer is valid
        self.assertEqual(serializer.validated_data['title'], "Test Post") # Ensure the title is correct