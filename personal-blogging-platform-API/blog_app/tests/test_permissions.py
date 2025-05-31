from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from blog_app.models import Post, Category, Tag
from django.urls import reverse
from rest_framework import status

class AuthTestCase(APITestCase):
    """
    Tests user registration and authentication endpoints.
    Sets up a test user for use in authentication-related tests.
    """
    def setUp(self):
        self.register_url = reverse('register') # /register/
        self.login_url = reverse('token_obtain_pair') # /api/login/
        self.refresh_url = reverse('token_refresh')  # /api/token/refresh/
        self.protected_url = reverse('post-list')  # /api/posts/

        # test data for creating or authenticating a user in API test
        self.user_data = {
            "username": "newuser",
            "password": "strongpassword123",
            "email": "newuser@example.com" 
        }

        # register user manually for token request
        self.user = User.objects.create_user(**self.user_data)

    
    def test_register_user(self):
        data = {
            "username": "testuser",
            "password": "testpass123",
            "email": "testuser@example.com"  
        }

        response = self.client.post(self.register_url, data, format="json") # try registering the user
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # will check if status is 201 created
        self.assertTrue(User.objects.filter(username="testuser").exists()) # will check if the user created exist


class PostUnauthenticatedAccessTest(APITestCase):
    """
    Tests that unauthenticated users can read posts
    but cannot create, update, or delete them.
    """
    def setUp(self):
        self.user = User.objects.create_user(username="owner", password="secret") # create a user
        self.category = Category.objects.create(name="Django") # create new category
        self.tag = Tag.objects.create(name="test") # create a new tag

        # create a new post
        self.post = Post.objects.create( 
            title = "Public post",
            content = "Anyone can read this.",
            author = self.user,
            category = self.category
        )
        self.post.tags.add(self.tag) # add tag to the post
        self.client = APIClient()
        self.create_url = reverse('post-list')  # /api/posts/
        self.detail_url = reverse('post-detail', kwargs={'slug': self.post.slug})  # /api/posts/<slug>/

    def test_guest_cannot_create_post(self):
        data = {
            "title": "New Post",
            "content": "Not Allowed",
            "category": self.category.name,
            "tags": [self.tag.name],
            "author": self.user.id
        }

        response = self.client.post(self.create_url, data, format='json') # try creating a new post
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # will check if status is 401 unathorized

    def test_guest_cannot_update_post(self):
        data = {
            "title": "Hack",
            "content": "Not yours",
            "category": self.category.name,
            "tags": [self.tag.name],
            "author": self.user.id
        }

        response = self.client.put(self.detail_url, data, format='json') # try updating an existing post
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # will check if status is 401 unathorized

    def test_guest_cannot_delete_post(self):
        response = self.client.delete(self.detail_url) # try deleting an existing post
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # will check if status is 401 unathorized



class PostPermissionTest(APITestCase):
    """
    Tests that non owner users can read posts
    but cannot update or delete the owners post.
    """
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="secret") # create a new user -> owner
        self.other_user = User.objects.create_user(username="intruder", password="intrude") # create another user -> hacker
        self.category = Category.objects.create(name="Django") # create a category
        self.tag = Tag.objects.create(name="test") # create a tag

        # create a new post with owner = owner
        self.post = Post.objects.create(
            title="Owner's Post",
            content="Protected",
            author=self.owner,
            category=self.category
        )
        self.post.tags.add(self.tag) # add tag to post
        self.client = APIClient()
        self.detail_url = reverse('post-detail', kwargs={'slug': self.post.slug}) # /api/posts/<slug>/


    def test_non_owner_cannot_update_post(self):
        self.client.force_authenticate(user=self.other_user) # force authentication for other_user

        data = {
            "title": "Hacked",
            "content": "Trying to update",
            "category": self.category.name,
            "tags": [self.tag.name],
            "author": self.owner.id
        }
        response = self.client.put(self.detail_url, data, format='json') # try updating the data using other_user
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # will check if status is 403 forbidden

    def test_non_owner_cannot_delete_post(self):
        self.client.force_authenticate(user=self.other_user) # force authentication for other_user
        response = self.client.delete(self.detail_url) # try deleting owners post using other_user
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # will check if status is 403 forbidden