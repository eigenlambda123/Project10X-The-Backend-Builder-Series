from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework import status
from shortener.models import ShortURL
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class ShortURLEdgeCaseTests(APITestCase):
    """
    Tests for edge cases in the ShortURL API.

    This test class verifies:
    - Creating a short URL without the required original_url field returns HTTP 400 Bad Request
    - Creating a short URL with an invalid original_url returns HTTP 400 Bad Request
    - Creating a short URL with a duplicate custom short_code returns HTTP 400 Bad Request
    - Updating editable fields (like short_code) is allowed, while non-editable fields (like clicks and created_at) remain unchanged

    """
    def setUp(self):
        self.user = User.objects.create_user(username="edgeuser", password="edgepass") # create a dummy user 
        refresh = RefreshToken.for_user(self.user) # create a refresh token for the dummy user
        self.access_token = str(refresh.access_token) # get the access token from the refresh token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token) # set the authorization header with the access token
        self.url_list = reverse("shorturl-list") # URL for the list of short URLs

    def test_missing_original_url_returns_400(self):
        """
        Test that creating a short URL without an original_url field returns HTTP 400 Bad Request
        """
        response = self.client.post(self.url_list, {}, format="json") # send a POST request without original_url
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # check if status 400 BAD REQUEST
        self.assertIn("original_url", response.data) # check if the response data contains original_url error

    def test_invalid_url_returns_400(self):
        """
        Test that creating a short URL with an invalid original_url returns HTTP 400 Bad Request
        """
        response = self.client.post(self.url_list, {"original_url": "not_a_url"}, format="json") # send a POST request with an invalid URL
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # check if status 400 BAD REQUEST
        self.assertIn("original_url", response.data) # check if the response data contains original_url error


    def test_duplicate_manual_short_code_returns_400(self):
        """
        Test that creating a short URL with a duplicate custom short_code returns HTTP 400 BAD REQUEST
        """

        # Create a short URL with a custom short code
        shorturl = ShortURL.objects.create(
            user=self.user,
            original_url="https://example.com",
            short_code="custom123"
        )
        # Attempt to create another short URL with the same custom short code
        response = self.client.post(
            self.url_list,
            {"original_url": "https://another.com", "short_code": "custom123"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # check if status 400 BAD REQUEST
        self.assertIn("short_code", response.data) # check if the response data contains short_code error


    
    def test_updating_non_editable_and_editable_fields(self):
        """
        Test that updating editable and non-editable fields via PATCH behaves correctly:
        - `short_code` should be updatable.
        - `clicks` and `created_at` should remain unchanged.
        """

        # Create a short URL with initial values
        shorturl = ShortURL.objects.create(
            user=self.user,
            original_url="https://example.com",
            short_code="initialcode",
            clicks=0
        )
        original_created_at = shorturl.created_at # Store the original created_at for later comparison

        url_detail = reverse("shorturl-detail", args=[shorturl.id]) # Get the detail URL for the created short URL

        # Attempt to update the short_code and clicks
        payload = {
            "clicks": 999,
            "created_at": timezone.now().isoformat(),
            "short_code": "updatedcode"
        }

        response = self.client.patch(url_detail, payload, format="json") # send a PATCH request to update the short URL
        self.assertEqual(response.status_code, status.HTTP_200_OK) # check if status 200 OK

        shorturl.refresh_from_db() # Refresh the short URL instance from the database
        self.assertEqual(shorturl.short_code, "updatedcode")  # updating short code should be allowed
        self.assertNotEqual(shorturl.clicks, 999)  # updating clicks should not change
        self.assertEqual(shorturl.clicks, 0) # Should remain unchanged
        self.assertEqual(shorturl.created_at, original_created_at)  # Should remain unchanged


