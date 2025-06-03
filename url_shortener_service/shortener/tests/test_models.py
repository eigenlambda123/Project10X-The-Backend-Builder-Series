from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from shortener.models import ShortURL

class ShortURLModelTest(TestCase):
    """
    """

    def setUp(self):
        self.valid_url = "https://example.com"
        self.expiration_date = timezone.now() + timedelta(days=1)

    def test_create_shorturl_with_required_fields(self):
        """
        Test if creating a short url is working with the required fields
        """

        # create a short url
        url = ShortURL.objects.create(
            original_url=self.valid_url
        )
        self.assertEqual(url.original_url, self.valid_url) # check if the original_url is correctly using valid_url as its value
        self.assertTrue(url.short_code) # check if short_code is created
        self.assertEqual(url.clicks, 0) # check how many clicks, should be 0


    def test_created_at_is_auto_generated(self):
        """
        Test if the date the short url is created is auto generated
        """

        # create short url
        url = ShortURL.objects.create(
            original_url=self.valid_url
        )
        self.assertIsNotNone(url.created_at) # check if created_at is created
        self.assertAlmostEqual(url.created_at.timestamp(), timezone.now().timestamp(), delta=2)
