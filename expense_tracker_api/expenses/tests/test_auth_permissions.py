from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class AuthPermissionTests(APITestCase):
    def test_user_can_register_successfully(self):
        url = reverse('register') # access register url endpoint

        # input data
        data = {
            'username': 'testuser',
            'email': 'testemail@gmail.com',
            'password': 'strongpassword123'
        }

        response = self.client.post(url, data) # access register with APICLient and post the data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # check if status 201 created
        self.assertTrue(User.objects.filter(username='testuser').exists()) # check if the user is created successfully
