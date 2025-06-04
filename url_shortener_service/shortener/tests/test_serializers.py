from django.test import TestCase
from django.utils import timezone
from shortener.serializers import ShortURLSerializer
from shortener.models import ShortURL
from datetime import timedelta

class ShortURLSerializerTest(TestCase):
    """
    """
    def setUp(self):
        self.valid_url = "https://example.com" # dummy url
        self.future_date = timezone.now() + timedelta(days=1) 
        self.past_date = timezone.now() - timedelta(days=1) 

    def test_valid_original_url_is_accepted(self):
        """
        Test for accepting valid url
        """
        serializer = ShortURLSerializer(data={"original_url": self.valid_url}) # serialize dummy url
        self.assertTrue(serializer.is_valid(), serializer.errors) # check if dummy url is valid

    def test_invalid_url_is_rejected(self):
        """
        Test if invalid url is rejected
        """
        invalid_url = "not-a-valid-url" # invalid dummy url
        serializer = ShortURLSerializer(data={"original_url": invalid_url}) # serialize invalid url
        self.assertFalse(serializer.is_valid()) # check if not valid
        self.assertIn("original_url", serializer.errors) # check if the error involves original_url