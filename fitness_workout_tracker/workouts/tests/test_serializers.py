from django.test import TestCase
from django.contrib.auth import get_user_model
from workouts.serializers import WorkoutSerializer
from workouts.models import Workout
from datetime import date

User = get_user_model()

class WorkoutSerializerTest(TestCase):
    """
    """
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass123') # create dummy user

    def test_valid_workout_data(self):
        """
        Test that the WorkoutSerializer validates correct data
        """

        # create a valid workout data
        data = {
            "name": "Upper Body Session",
            "date": str(date.today()),
            "notes": "Felt strong today!"
        }
        serializer = WorkoutSerializer(data=data) # Initialize the serializer with the data
        self.assertTrue(serializer.is_valid()) # check if valid 

    