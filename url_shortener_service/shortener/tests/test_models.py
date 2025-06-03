from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from shortener.models import ShortURL
import uuid

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


    def test_clicks_default_to_zero(self):
        """
        Test if clicks starts at 0
        """

        # create short url
        url = ShortURL.objects.create(
            original_url=self.valid_url
        )
        self.assertEqual(url.clicks, 0) # check if clicks == 0

    def test_optional_expiration_date(self):
        """
        Test if expiration date is set properly
        """

        # create short url
        url = ShortURL.objects.create(
            original_url=self.valid_url,
            expiration_date=self.expiration_date
        )
        self.assertEqual(url.expiration_date, self.expiration_date) # check if expiration_date is using the correct value
    

    def test_str_method_returns_expected_string(self):
        """
        Test if str method is returning correct short url
        """
        # create short url with a unique short_code
        unique_code = str(uuid.uuid4())[:8] 
        url = ShortURL.objects.create(
            original_url=self.valid_url,
            short_code=unique_code
        )
        expected_str = f"{unique_code} → https://example.com"
        self.assertEqual(str(url), expected_str) # check if returning correct url