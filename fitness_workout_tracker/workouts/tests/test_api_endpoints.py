from workouts.views import WorkoutViewSet
from django.test import TestCase
from rest_framework.test import APIClient


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

    

        

