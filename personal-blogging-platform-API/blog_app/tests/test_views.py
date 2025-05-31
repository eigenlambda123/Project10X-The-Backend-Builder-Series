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

    def test_get_post_list(self):
        response = self.client.get(self.create_url) # get post-list via create_url
        self.assertEqual(response.status_code, status.HTTP_200_OK) # check if the reponse status code is 200 ok 
        self.assertGreaterEqual(len(response.data), 1) # checks that the response from the API contains at least one post in the list

    def test_get_single_post(self):
        response = self.client.get(self.detail_url) # get post-detail via detail_url
        self.assertEqual(response.status_code, status.HTTP_200_OK) # check if the reponse status code is 200 ok 
        self.assertEqual(response.data['slug'], self.post.slug) # ensures that the api returns the correct post for the given slug

    def test_update_post(self):
        # updates the created data title and content
        data = {
            "title": "Updated Title",
            "content": "Updated content.",
            "category": self.category.name,
            "tags": [self.tag.name],
            "author": self.user.id
        }
        response = self.client.put(self.detail_url, data, format='json') # sends a PUT request to the API to update an existing post
        self.assertEqual(response.status_code, status.HTTP_200_OK) # check if the reponse status code is 200 ok 
        self.assertEqual(response.data['title'], "Updated Title") # check if the current title is equal to the updated title
