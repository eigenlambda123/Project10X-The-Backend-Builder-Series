from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from workouts.models import Workout
from rest_framework import status

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


    def test_unauthenticated_access_is_denied(self):
        """
        Test that unauthenticated users cannot access workout endpoints
        """
        response = self.client.get(self.workout_list_url) # Attempt to access the workout list without authentication
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Check if the response status is 401 Unauthorized

        # Attempt to send a POST request without authentication
        response = self.client.post(self.workout_list_url, {
            "name": "Anonymous Workout",
            "date": "2023-10-02"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Check if the response status is 401 Unauthorized

        response = self.client.get(self.workout_detail_url) # Attempt to access the workout detail without authentication
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Check if the response status is 401 Unauthorized


    def test_authenticated_user_can_only_access_own_workouts(self):
        """
        Test that authenticated users can only access their own workouts
        """

        self.client.force_authenticate(user=self.user2) # Authenticate as user2

        # Try to retrieve user1's workout
        response = self.client.get(self.workout_detail_url) # Attempt to get user1's workout
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) # Check if the response status is 404 Not Found

        # Try to update user1's workout
        response = self.client.put(self.workout_detail_url, {
            "name": "Hacked Workout",
            "date": "2023-10-05"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) # Check if the response status is 404 Not Found

        # Try to delete user1's workout
        response = self.client.delete(self.workout_detail_url) # Attempt to delete user1's workout
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) # Check if the response status is 404 Not Found
