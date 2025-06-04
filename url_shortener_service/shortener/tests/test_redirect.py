from rest_framework.test import APITestCase
from shortener.models import ShortURL
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

class RedirectViewTest(APITestCase):
    """
    Tests for the redirect endpoint of the URL shortener service

    This test class verifies:
    - A valid short code issues an HTTP 302 redirect to the original URL
    - An invalid (non-existent) short code returns HTTP 404 Not Found
    - An expired short code returns HTTP 410 Gone with an appropriate error message

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

    def test_expired_short_code_returns_410(self):
        """
        Test that an expired short code returns HTTP 410 Gone or a custom error
        """

        # created an expired short URL
        expired_url = ShortURL.objects.create(
            original_url="https://expired.com",
            expiration_date=timezone.now() - timedelta(days=1)
        )

        url = reverse("redirect", args=[expired_url.short_code]) # reverse the URL for the redirect view using the expired short code
        response = self.client.get(url) # send a GET request to the redirect URL with the expired short code

        self.assertEqual(response.status_code, status.HTTP_410_GONE) # check if the status code is 410 Gone
        self.assertIn("expired", response.data["detail"].lower()) # check if the response contains an expired message in the detail field



class ClickTrackingTest(APITestCase):
    """
    """

    def setUp(self):
        # create a dummy short URL 
        self.shorturl = ShortURL.objects.create(
            original_url="https://clicks.com",
            short_code="track123",
            expiration_date=timezone.now() + timedelta(days=7),
        )
        self.redirect_url = reverse("redirect", args=[self.shorturl.short_code]) # reverse the URL for the redirect view using the short code

    def test_click_count_increments_on_redirect(self):
        """
        Test that confirm click count increases on each redirect access
        """

        initial_clicks = self.shorturl.clicks # initial click count before redirects
        num_redirects = 3 # number of redirects to simulate

        for _ in range(num_redirects): # simulate multiple redirects
            response = self.client.get(self.redirect_url) # send a GET request to the redirect URL
            self.assertEqual(response.status_code, status.HTTP_302_FOUND) # check if the status code is 302 Found

        self.shorturl.refresh_from_db() # refresh the ShortURL instance from the database to get the updated click count
        self.assertEqual(self.shorturl.clicks, initial_clicks + num_redirects) # check if the click count has increased by the number of redirects