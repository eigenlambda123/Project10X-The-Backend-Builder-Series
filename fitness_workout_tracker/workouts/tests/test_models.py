from django.test import TestCase
from django.contrib.auth.models import User


class WorkoutModelTest(TestCase):
    """
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass') # create dummy user