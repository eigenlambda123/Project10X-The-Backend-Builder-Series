from workouts.views import WorkoutViewSet
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class WorkoutEndpointTests(TestCase):
    """
    """
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/workouts/' # url for the WorkoutViewSet]
        self.test_workout_data = {
            "name": "Test Workout",
            "date": "2023-10-01",
            "notes": "This is a test workout."
        }

    def test_create_workout(self):
        """
        Test creating a new workout via the API endpoint
        """
        response = self.client.post(self.url, self.test_workout_data, format='json') # send POST request to create a new workout
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # check if status 201 CREATED
        self.assertEqual(response.data['name'], self.test_workout_data['name']) # check if the name matches the test data

    

        

