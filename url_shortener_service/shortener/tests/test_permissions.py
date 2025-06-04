from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

class ShortURLPermissionTest(APITestCase):
    """
    """
    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username='user1', password='pass1234')
        self.user2 = User.objects.create_user(username='user2', password='pass1234')

        # Authenticate user1
        refresh = RefreshToken.for_user(self.user1)
        self.access_token_user1 = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_user1)

        self.url_list = reverse('user_urls') # URL for listing user URLs

        # Create a valid payload for creating a short URL
        self.valid_payload = {
            "original_url": "https://example.com"
        }

