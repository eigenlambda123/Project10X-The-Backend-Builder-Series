from django.test import TestCase
from django.contrib.auth.models import User
from blog_app.models import Post, Category, Tag

class PostModelTest(TestCase):
    """
    Test case for the Post model.
    """
    def setUp(self):
        """
        Set up the test environment by creating a user, category, and tag.
        """
        self.user = User.objects.create_user(username="testuser", password="secret123")
        self.category = Category.objects.create(name="Django")
        self.tag = Tag.objects.create(name="testing")
