from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from blog_app.models import Post, Category, Tag
from django.urls import reverse
from rest_framework import status

class PostTestAPI(APITestCase):
    """
    Test case for the Post API endpoints.
    """

    def setUp(self):
        """
        Set up the test environment by creating a client.
        """
        self.client = APIClient() # Initialize the API client for testing
        self.user = User.objects.create_user(username="testuser", password="secret123") # Create a test user
        self.category = Category.objects.create(name="Django") # Create a test category
        self.tag = Tag.objects.create(name="testing") # Create a test tag
        self.client.force_authenticate(user=self.user) # Authenticate the client with the test user

        # Create a Post instance for testing
        self.post = Post.objects.create(
            title="Test Post",
            content="This is a test post content.",
            author=self.user,
            category=self.category
        )
        self.post.tags.add(self.tag) # Add the tag to the post

        self.create_url = reverse('post-list')  # /api/posts/
        self.detail_url = reverse('post-detail', kwargs={'slug': self.post.slug})  # /api/posts/<slug>/

    
    def test_create_post(self):
        """
        Test creating a new post via the API.
        """ 
        # Prepare the data for creating a new post
        data = {
            "title": "New Post",
            "content": "This is a new post content.",
            "category": self.category.name,
            "tags": [self.tag.name],
            "author": self.user.id  # Add this line if required
        }
        response = self.client.post(self.create_url, data, format='json') # Send a POST request to create a new post
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # Check if the response status code is 201 Created
        self.assertEqual(response.data['title'], "New Post") # Check if the title in the response matches the created post title

