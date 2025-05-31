from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from blog_app.models import Post, Category, Tag
from django.urls import reverse
from rest_framework import status

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

