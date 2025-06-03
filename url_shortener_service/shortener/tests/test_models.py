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
