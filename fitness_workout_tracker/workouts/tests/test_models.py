from django.test import TestCase
from django.contrib.auth.models import User
from workouts.models import Workout, Exercise
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



