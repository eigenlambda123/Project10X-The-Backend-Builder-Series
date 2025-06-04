from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework import status
from shortener.models import ShortURL

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

        self.url_list = reverse('shorturl-list') # URL for the list of short URLs

        # Create a valid payload for creating a short URL
        self.valid_payload = {
            "original_url": "https://example.com"
        }

    def test_unauthenticated_post_fails(self):
        """
        Test that an authenticated user cannot create a short URL
        """
        self.client.credentials()  # Remove auth header
        response = self.client.post(self.url_list, self.valid_payload, format='json') # make a POST request to create a short URL
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # check if status 401 UNAUTHORIZED

    def test_authenticated_user_can_create_and_view_own_links(self):
        """
        Test that an authenticated user can create a short URL and view their own links
        """

        # user 1 creates a short URL
        post_response = self.client.post(self.url_list, self.valid_payload, format='json') # make a POST request to create a short URL
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED) # check if status 201 CREATED


        # User1 retrieves their link
        get_response = self.client.get(self.url_list) # make a GET request to retieve the list of short URLs
        self.assertEqual(get_response.status_code, status.HTTP_200_OK) # check if status 200 OK
        self.assertEqual(len(get_response.data["results"]), 1) # check if one short URL is returned
        self.assertEqual(get_response.data["results"][0]["original_url"], "https://example.com") # check if the original URL matches


    def test_user_cannot_delete_others_links(self):
        """
        Test that a user cannot delete another user's short URL
        """
        # User1 creates a short URL
        short_url = ShortURL.objects.create(user=self.user1, original_url="https://private.com")

        # Authenticate as user2
        refresh = RefreshToken.for_user(self.user2) # Create a refresh token for user2
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token)) # Authenticate user2


        # Try to delete user1's short URL
        url_detail = reverse("shorturl-detail", args=[short_url.id]) # GET the detail URL for the short URL created by user 1
        response = self.client.delete(url_detail) # try deleting the url_detail created by user 1 with user 2
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # check if status 403 FORBIDDEN


