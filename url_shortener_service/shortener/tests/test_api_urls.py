from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class ShortURLAPITest(APITestCase):
    """
    """
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123") # created dummy user
        refresh = RefreshToken.for_user(self.user) # create a refresh token for the user
        self.access_token = str(refresh.access_token) # get the access token from the refresh token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token) # set the authorization header with the access token
        self.url_list = reverse('shorturl-list')  # /api/urls/

        # valid payload for creating a short URL
        self.valid_payload = {
            "original_url": "https://example.com"
        }

    def test_create_short_url(self):
        """
        Test if creating a short URL is successful
        """
        response = self.client.post(self.url_list, self.valid_payload, format='json') # send a POST request to url_list with valid_payload
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # check if status 201 created
        self.assertIn("short_code", response.data) # check if short_code is in response data
        self.assertEqual(response.data["original_url"], self.valid_payload["original_url"]) # check if original_url is response data matches valid_payload
        self.assertEqual(response.data["clicks"], 0) # chec if clicks is added and is 0