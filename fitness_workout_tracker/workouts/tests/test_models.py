from django.test import TestCase
from django.contrib.auth.models import User
from workouts.models import Workout
from datetime import date


class WorkoutModelTest(TestCase):
    """
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