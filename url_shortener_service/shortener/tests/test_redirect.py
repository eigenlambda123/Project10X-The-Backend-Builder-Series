from rest_framework.test import APITestCase
from shortener.models import ShortURL
from django.urls import reverse
from rest_framework import status

class RedirectViewTest(APITestCase):
    """
    """

    def setUp(self):
        self.valid_url = "https://example.com" # dummy valid URL
        self.short = ShortURL.objects.create(original_url=self.valid_url) # create a ShortURL instance with the dummy valid URL

    def test_valid_short_code_redirects(self):
        """
        Test that a valid short code returns HTTP 302 and redirects to original_url
        """
        url = reverse("redirect", args=[self.short.short_code]) # reverse the URL for the redirect view using the short code
        response = self.client.get(url) # send a GET request to the redirect URL

        self.assertEqual(response.status_code, status.HTTP_302_FOUND) # check if the status code is 302 Found
        self.assertEqual(response["Location"], self.valid_url) # check if the Location header matches the original URL

    def test_invalid_short_code_returns_404(self):
        """
        Test that a non-existent short code returns HTTP 404 Not Found
        """
        url = reverse("redirect", args=["nonexistent"]) # reverse the URL for the redirect view using a non-existent short code
        response = self.client.get(url) # send a GET request to the redirect URL with the non-existent short code

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # check if the status code is 404 Not Found