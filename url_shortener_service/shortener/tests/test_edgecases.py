from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


User = get_user_model()

class ShortURLEdgeCaseTests(APITestCase):
    """
    """
    def setUp(self):
        self.user = User.objects.create_user(username="edgeuser", password="edgepass") # create a dummy user 
        refresh = RefreshToken.for_user(self.user) # create a refresh token for the dummy user
        self.access_token = str(refresh.access_token) # get the access token from the refresh token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token) # set the authorization header with the access token
        self.url_list = reverse("shorturl-list") # URL for the list of short URLs

        