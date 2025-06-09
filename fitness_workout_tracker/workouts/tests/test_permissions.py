from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from workouts.models import Workout

User = get_user_model()

class WorkoutPermissionTests(TestCase): 
    """
    """
    def setUp(self):
        self.client = APIClient() # Create an API client for testing
        self.user1 = User.objects.create_user(username='user1', password='pass123') # create dummy user1
        self.user2 = User.objects.create_user(username='user2', password='pass123') # create dummy user2

        # Workout owned by user1
        self.workout = Workout.objects.create(
            user=self.user1, # Associate workout with user1
            name='User1 Workout',
            date='2023-10-01',
            notes='Owned by user1'
        )
        self.workout_detail_url = reverse('workout-detail', args=[self.workout.id]) # URL for the workout detail view
        self.workout_list_url = reverse('workout-list') # URL for the workout list view