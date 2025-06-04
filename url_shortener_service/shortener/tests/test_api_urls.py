from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class ShortURLAPITest(APITestCase):
    """
    """
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123") # created dummy user
        self.client.login(username="testuser", password="testpass123") # login with dummy user
        self.url_list = reverse('shorturl-list')  # /api/urls/

        # valid payload for creating a short URL
        self.valid_payload = {
            "original_url": "https://example.com"
        }