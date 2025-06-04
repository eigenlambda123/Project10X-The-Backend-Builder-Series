from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from shortener.models import ShortURL
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

class ShortURLAPITest(APITestCase):
    """
    API integration tests for the ShortURL endpoints.

    This test class verifies the following behaviors:
    - Authenticated creation of short URLs via POST
    - Retrieval of a user's short URL list, including pagination handling
    - Retrieval of individual short URL details
    - Deletion of short URLs
    - Partial updates (PATCH) to short URLs, such as updating expiration dates
    - Validation that creating a short URL with an invalid original URL returns a 400 Bad Request
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


    def test_get_url_list(self):
        """
        Test if retrieving the list of URLs works correctly
        """
        ShortURL.objects.create(user=self.user, original_url="https://abc.com") # create a short URL 1
        ShortURL.objects.create(user=self.user, original_url="https://xyz.com") # create a short URL 2

        response = self.client.get(self.url_list) # send a GET request to url_list
        self.assertEqual(response.status_code, status.HTTP_200_OK) # check if status 200 OK
        
        # Handle paginated response
        data = response.data["results"] if "results" in response.data else response.data # check if the response data is paginated, if so get the results, otherwise get the data directly

        user_urls = [item for item in data if item['original_url'] in ["https://abc.com", "https://xyz.com"]] # filter the response data to get URLs created by the user
        self.assertEqual(len(user_urls), 2) # check if the number of URLs returned is 2


    def test_get_url_detail(self):
        """
        Test if retrieving the details of a specific short URL works correctly
        """
        shorturl = ShortURL.objects.create(user=self.user, original_url="https://abc.com") # create new dummy short URL
        url_detail = reverse("shorturl-detail", args=[shorturl.id]) # get the detail URL for the created short URL via id
        response = self.client.get(url_detail) # send a GET request to the detail URL

        self.assertEqual(response.status_code, status.HTTP_200_OK) # check if status 200 OK
        self.assertEqual(response.data["original_url"], "https://abc.com") # check if original_url in response data matches the created short URL
        self.assertIn("short_code", response.data) # check if short_code is in response data

    def test_delete_short_url(self):
        """
        Test if deleting a short URL works correctly
        """
        shorturl = ShortURL.objects.create(user=self.user, original_url="https://delete.com") # create a new dummy short URL to delete
        url_detail = reverse("shorturl-detail", args=[shorturl.id]) # get the detail URL for the created short URL via id
        response = self.client.delete(url_detail) # send a DELETE request to the detail URL

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) # check if status 204 no content
        self.assertFalse(ShortURL.objects.filter(id=shorturl.id).exists()) # check if the short URL is successfully deleted

    def test_update_short_url_patch(self):
        """
        Test if updating a short URL's expiration date works correctly
        """
        shorturl = ShortURL.objects.create(user=self.user, original_url="https://initial.com") # create a new dummy short URL to update
        new_expiry = timezone.now() + timedelta(days=7) # set a new expiration date 7 days in the future
        url_detail = reverse("shorturl-detail", args=[shorturl.id]) # get the detail URL for the created short URL via id
        response = self.client.patch(url_detail, {"expiration_date": new_expiry}, format="json") # send a PATCH request to update the expiration date

        self.assertEqual(response.status_code, status.HTTP_200_OK) # check if status 200 OK
        self.assertEqual(response.data["expiration_date"][:10], new_expiry.date().isoformat()) # check if the expiration date in response data matches the new expiration date


    def test_create_with_invalid_url_returns_400(self):
        """
        Test if creating a short URL with an invalid original URL returns a 400 Bad Request
        """

        bad_payload = {"original_url": "invalid-url"} # invalid URL payload
        response = self.client.post(self.url_list, bad_payload, format='json') # send a POST request with the invalid payload
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # check if status 400 Bad Request 
        self.assertIn("original_url", response.data) # check if the error involves original_url