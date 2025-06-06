from django.test import TestCase
from django.contrib.auth import get_user_model
from workouts.serializers import WorkoutSerializer
from workouts.models import Workout, Set
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

    def test_sets_field_is_read_only_nested(self):
        """
        Test that the 'sets' field in the WorkoutSerializer is read-only and returns a list
        """
        
        workout = Workout.objects.create(user=self.user, name="Push Day", date=date.today()) # create a workout 
        Set.objects.create(workout=workout, exercise=None, reps=10, order=1) # create a set for the workout
        serializer = WorkoutSerializer(workout) # Initialize the serializer with the workout instance
        self.assertIn('sets', serializer.data) # check if 'sets' field is in the serialized data
        self.assertIsInstance(serializer.data['sets'], list) # check if 'sets' field is a list
     

    