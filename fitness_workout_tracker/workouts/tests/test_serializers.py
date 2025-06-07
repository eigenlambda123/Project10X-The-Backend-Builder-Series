from django.test import TestCase
from django.contrib.auth import get_user_model
from workouts.serializers import WorkoutSerializer, SetSerializer
from workouts.models import Workout, Set, Exercise
from datetime import date

User = get_user_model()

class WorkoutSerializerTest(TestCase):
    """
    Unit tests for the WorkoutSerializer.

    This test case verifies:
    - The serializer correctly validates valid and invalid workout data
    - Required fields are enforced and missing fields raise validation errors
    - The 'name' field cannot be blank
    - The 'sets' field is read-only and returns a list of related sets
    - The 'user' field is read-only and cannot be set via input data
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
        exercise = Exercise.objects.create(name="Bench Press", category="push") # create an exercise
        Set.objects.create(workout=workout, exercise=exercise, reps=10, order=1) # create a set for the workout
        serializer = WorkoutSerializer(workout) # Initialize the serializer with the workout instance
        self.assertIn('sets', serializer.data) # check if 'sets' field is in the serialized data
        self.assertIsInstance(serializer.data['sets'], list) # check if 'sets' field is a list

    def test_user_field_is_read_only(self):
        """
        Test that the 'user' field in the WorkoutSerializer is read-only
        """

        # create a valid workout data without user
        data = {
            "name": "Leg Day",
            "date": str(date.today()),
            "user": self.user.id
        }
        serializer = WorkoutSerializer(data=data) # Initialize the serializer with the data
        self.assertTrue(serializer.is_valid()) # check if valid
        self.assertNotIn('user', serializer.validated_data) # check if 'user' field is not in the validated data



class SetSerializerTest(TestCase):
    """
    """
    def setUp(self):
        self.user = User.objects.create_user(username='tester2', password='pass123') # create dummy user
        self.workout = Workout.objects.create(user=self.user, name="Pull Day", date=date.today()) # create a workout 
        self.exercise = Exercise.objects.create(name="Pull-up", category="upper") # create an exercise


    def test_valid_set_data(self):
        """
        Test that the SetSerializer validates correct set data
        """

        # valid set data
        data = {
            "workout": self.workout.id,
            "exercise": self.exercise.id,
            "reps": 8,
            "order": 1
        }
        serializer = SetSerializer(data=data) # serialize the data
        self.assertTrue(serializer.is_valid()) # check if valid


    def test_optional_fields_accepted(self):
        """
        Test that the SetSerializer accepts optional fields like weight, duration, and notes
        """

        # valid set data with optional fields
        data = {
            "workout": self.workout.id,
            "exercise": self.exercise.id,
            "reps": 12,
            "order": 2,
            "weight": None,
            "duration": None,
            "notes": ""
        }
        serializer = SetSerializer(data=data) # serialize the data
        self.assertTrue(serializer.is_valid()) # check if valid

    def test_negative_reps_invalid(self):
        """
        Test that the SetSerializer raises validation error for negative reps
        """

        # data with negative reps
        data = {
            "workout": self.workout.id,
            "exercise": self.exercise.id,
            "reps": -5,
            "order": 1
        }
        serializer = SetSerializer(data=data) # serialize the data
        self.assertFalse(serializer.is_valid()) # check if invalid
        self.assertIn('reps', serializer.errors) # check if the error involves reps


    def test_negative_order_invalid(self):
        """
        Test that the SetSerializer raises validation error for negative order
        """

        # data with negative order
        data = {
            "workout": self.workout.id,
            "exercise": self.exercise.id,
            "reps": 10,
            "order": -2
        }
        serializer = SetSerializer(data=data) # serialize the data
        self.assertFalse(serializer.is_valid()) # check if invalid
        self.assertIn('order', serializer.errors) # check if the error involves order


    def test_read_only_exercise_name(self):
        """
        Test that the 'exercise_name' field in SetSerializer is read-only and returns the exercise name
        """

        # create a set instance
        set_instance = Set.objects.create(
            workout=self.workout,
            exercise=self.exercise,
            reps=10,
            order=1
        )
        serializer = SetSerializer(set_instance) # serialize the set instance
        self.assertEqual(serializer.data['exercise_name'], "Pull-up") # check if 'exercise_name' field returns the correct exercise name


    