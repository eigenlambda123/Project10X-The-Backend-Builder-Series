from django.contrib.auth import get_user_model
from workouts.views import WorkoutViewSet
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

User = get_user_model()

class WorkoutEndpointTests(TestCase):
    """
    """
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('workout-list') # dynamically resolve the URL for the WorkoutViewSet
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass') # create a dummy user for authentication
        self.client.force_authenticate(user=self.user) # authenticate the client with the test user
        self.test_workout_data = {
            "user": self.user.id,  
            "name": "Test Workout",
            "date": "2023-10-01",
            "notes": "This is a test workout."
        }

    def test_create_workout(self):
        """
        Test creating a workout via the API endpoint
        """

        # data 
        response = self.client.post(self.url, {
            "name": self.test_workout_data["name"],
            "date": self.test_workout_data["date"],
            "notes": self.test_workout_data["notes"],
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # check if status code is 201 CREATED

        # check if the response data matches the input data
        self.assertEqual(response.data['name'], self.test_workout_data['name'])
        self.assertEqual(response.data['notes'], self.test_workout_data['notes'])
        self.assertEqual(response.data['date'], self.test_workout_data['date'])
        self.assertEqual(response.data['user'], self.user.id) 


    

        

