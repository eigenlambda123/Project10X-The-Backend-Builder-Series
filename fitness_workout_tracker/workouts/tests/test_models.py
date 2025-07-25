from django.test import TestCase
from django.contrib.auth.models import User
from workouts.models import Workout, Exercise, Set
from datetime import date


class WorkoutModelTest(TestCase):
    """
    Unit tests for the Workout model.

    This test case verifies:
    - Creation of Workout instances with required and optional fields
    - That the notes field can be left blank or None
    - The string representation (__str__) of the Workout model returns the expected format
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass') # create dummy user

    def test_create_workout_with_required_fields(self):
        """
        Test creating a Workout instance with required fields
        """
        workout = Workout.objects.create(user=self.user, name='Leg Day', date=date.today()) # create a workout
        self.assertEqual(workout.user, self.user) # check if the user is set correctly
        self.assertEqual(workout.name, 'Leg Day') # check if the name is set correctly
        self.assertEqual(workout.date, date.today()) # check if the date is set correctly
        self.assertIsNone(workout.notes) # check if the note is none by default


    def test_optional_notes_field_accepts_blank(self):
        """
        Test that the notes field can be blank
        """
        workout = Workout.objects.create(user=self.user, name='Push Day', date=date.today(), notes='') # create a workout with empty notes
        self.assertEqual(workout.notes, '') # check if the notes are empty

    def test_str_method_returns_expected_format(self):
        """
        Test if the __str__ method returns the expected format
        """
        workout = Workout.objects.create(user=self.user, name='Pull Day', date=date(2025, 6, 6)) # create a workout with specific date
        self.assertEqual(str(workout), "Pull Day - testuser (2025-06-06)") # check if the string representation is correct



class ExerciseModelTest(TestCase):
    """
    Unit tests for the Exercise model.

    This test case verifies:
    - Creation of Exercise instances with required fields
    - That the default category is 'other' when not specified
    - The description field can be left blank or None
    - The string representation (__str__) of the Exercise model returns the exercise name
    """

    def test_create_exercise_with_required_fields(self):
        """
        Test creating an Exercise instance with required fields
        """
        exercise = Exercise.objects.create(name='Deadlift', category='pull') # create an exercise with required fields
        self.assertEqual(exercise.name, 'Deadlift') # check if the name is set correctly
        self.assertEqual(exercise.category, 'pull') # check if the category is set correctly
        self.assertIsNone(exercise.description) # check if the description is none by default

    def test_default_category_is_other(self):
        """
        Test that the default category is 'other' when not specified
        """
        exercise = Exercise.objects.create(name='Unknown Move') # create an exercise without specifying category
        self.assertEqual(exercise.category, 'other') # check if the category is set to 'other' by default

    def test_optional_description_accepts_blank(self):
        """
        Test that the description field can be blank
        """
        exercise = Exercise.objects.create(name='Crunches', category='core', description='') # create an exercise with empty description
        self.assertEqual(exercise.description, '') # check if the description is empty

    def test_str_method_returns_exercise_name(self):
        """
        Test if the __str__ method returns the exercise name
        """
        exercise = Exercise.objects.create(name='Bench Press', category='push') # create an exercise with name 'Bench Press'
        self.assertEqual(str(exercise), 'Bench Press') # check if the string representation is correct


class SetModelTest(TestCase):
    """
    API endpoint for viewing and editing Set instances.

    Provides list, create, retrieve, update, and delete actions for sets
    Sets are ordered by their 'order' field by default
    """
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass') # create a dummy user
        self.workout = Workout.objects.create(user=self.user, name='Chest Day', date=date.today()) # create a workout for the user
        self.exercise = Exercise.objects.create(name='Incline Bench Press', category='push') # create an exercise for the workout

    def test_create_set_with_required_fields(self):
        """
        Test creating a Set instance with required fields
        """

        # create a Set instance with required fields
        set_obj = Set.objects.create(
            workout=self.workout,
            exercise=self.exercise,
            reps=10,
            order=1
        )
        
        self.assertEqual(set_obj.reps, 10) # check if the reps are set correctly
        self.assertEqual(set_obj.weight, None) # check if the weight is None by default
        self.assertEqual(set_obj.duration, None) # check if the duration is None by default
        self.assertEqual(set_obj.notes, None) # check if the notes are None by default


    def test_optional_fields_accept_null_or_blank(self):
        """
        Test that optional fields can be set to None or blank
        """

        # create a Set instance with optional fields set to None
        set_obj = Set.objects.create(
            workout=self.workout,
            exercise=self.exercise,
            reps=8,
            weight=None,
            duration=None,
            notes='',
            order=2
        )
        self.assertEqual(set_obj.notes, '') # check if the notes are empty
        self.assertIsNone(set_obj.weight) # check if the weight is None
        self.assertIsNone(set_obj.duration) # check if the duration is None

    def test_str_method_returns_formatted_string(self):
        """
        Test the string representation of the Set model
        """

        # create a Set instance
        set_obj = Set.objects.create(
            workout=self.workout,
            exercise=self.exercise,
            reps=12,
            weight=75.5,
            order=1
        )
        self.assertEqual(str(set_obj), "Incline Bench Press: 12 reps @ 75.5 lbs") # check if the string representation is correct

    def test_reps_and_order_must_be_positive_integers(self):
        """
        Test that reps and order must be positive integers
        """

        # Test that reps must be a positive integer
        with self.assertRaises(Exception):
            Set.objects.create(workout=self.workout, exercise=self.exercise, reps=-1, order=1)

        # Test that order must be a positive integer
        with self.assertRaises(Exception):
            Set.objects.create(workout=self.workout, exercise=self.exercise, reps=10, order=0)



