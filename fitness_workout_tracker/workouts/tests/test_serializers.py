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

    def test_missing_required_fields(self):
        """
        Test that the WorkoutSerializer raises validation error for missing required fields
        """
        data = {"notes": "Missing name and date"} # data with missing required fields
        serializer = WorkoutSerializer(data=data) # Initialize the serializer with the data
        self.assertFalse(serializer.is_valid()) # check if invalid
        self.assertIn('name', serializer.errors) # check if the error involves name
        self.assertIn('date', serializer.errors) # check if the error involves date

    def test_blank_name_invalid(self):
        """
        Test that the WorkoutSerializer raises validation error for the blank name
        """

        # data with blank name
        data = {
            "name": "",
            "date": str(date.today())
        }
        serializer = WorkoutSerializer(data=data) # Initialize the serializer with the data
        self.assertFalse(serializer.is_valid()) # check if invalid
        self.assertIn('name', serializer.errors) # check if the error involves name

    

    