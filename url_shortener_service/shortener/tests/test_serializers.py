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