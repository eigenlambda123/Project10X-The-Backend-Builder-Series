from django import Testcase
from django.contrib.auth.models import User
from expenses.models import Category

class CategoryModelTests(Testcase):
    """
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password') # create dummy user