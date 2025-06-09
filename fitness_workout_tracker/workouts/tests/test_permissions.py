from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from workouts.models import Workout, Set, Exercise
from rest_framework import status
from datetime import date

User = get_user_model()

class WorkoutPermissionTests(TestCase): 
    """
    Test suite for verifying workout API permissions

    - Ensures unauthenticated users cannot access or modify workouts (should receive 401 Unauthorized)
    - Ensures authenticated users can only access, update, or delete their own workouts (should receive 404 for others')
    - Ensures authenticated users cannot create workouts for other users (user field is set server-side)
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

    def test_authenticated_user_can_create_workout_and_user_is_set_server_side(self):
        """
        Test that authenticated users can create a workout and the user is set server-side
        """
        self.client.force_authenticate(user=self.user2) # Authenticate as user2

        # Create a new workout
        response = self.client.post(self.workout_list_url, {
            "name": "User2 Workout",
            "date": "2023-10-03",
            "user": self.user1.id  # attempt to assign another user
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # Check if the response status is 201 Created
        self.assertEqual(response.data['user'], self.user2.id) # Check if the user is set to user2, not user1


class TestSetPermission(TestCase):
    """
    Test suite for verifying Set API permissions.

    - Ensures unauthenticated users cannot access or modify sets (should receive 401 Unauthorized)
    - Ensures authenticated users can only create sets for their own workouts (should receive 403 Forbidden for others')
    - Ensures authenticated users cannot access, update, or delete sets belonging to other users (should receive 404 Not Found)
    """
    def setUp(self):
        self.client = APIClient() # Create an API client for testing
        self.user1 = User.objects.create_user(username='user1', password='pass123') # create dummy user1
        self.user2 = User.objects.create_user(username='user2', password='pass123') # create dummy user2

        self.exercise = Exercise.objects.create(name="Bench Press", category="push") # create an exercise
        self.workout_user1 = Workout.objects.create(user=self.user1, name="User1 Workout", date=date.today()) # create a workout for user1
        self.workout_user2 = Workout.objects.create(user=self.user2, name="User2 Workout", date=date.today()) # create a workout for user2

        # Create a set for user1's workout
        self.set_user1 = Set.objects.create(
            workout=self.workout_user1,
            exercise=self.exercise,
            reps=10,
            order=1
        )
        self.set_detail_url = reverse('set-detail', args=[self.set_user1.id]) # URL for the set detail view
        self.set_list_url = reverse('set-list') # URL for the set list view

    def test_unauthenticated_user_cannot_access_sets(self):
        """
        Test that unauthenticated users cannot access set endpoints
        """
        response = self.client.get(self.set_list_url) # Attempt to access the set list without authentication
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Check if the response status is 401 Unauthorized

        # Attempt to create a set without authentication
        response = self.client.post(self.set_list_url, {
            "workout": self.workout_user1.id,
            "exercise": self.exercise.id,
            "reps": 8,
            "order": 1
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Check if the response status is 401 Unauthorized

        response = self.client.get(self.set_detail_url) # Attempt to access the set detail without authentication
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Check if the response status is 401 Unauthorized

    def test_authenticated_user_can_only_create_sets_for_own_workouts(self):
        """
        Test that authenticated users can only create sets for their own workouts
        """
        self.client.force_authenticate(user=self.user2) # Authenticate as user2

        # Attempt to create set on user1's workout
        response = self.client.post(self.set_list_url, {
            "workout": self.workout_user1.id,
            "exercise": self.exercise.id,
            "reps": 12,
            "order": 2
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # Check if the response status is 403 Forbidden


    def test_user_cannot_access_or_modify_another_users_set(self):
        """
        Test that authenticated users cannot access or modify sets belonging to another user
        """
        self.client.force_authenticate(user=self.user2) # Authenticate as user2

        
        response = self.client.get(self.set_detail_url) # Attempt to access user1's set
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) # Check if the response status is 404 Not Found

        # Try to update user1's set
        response = self.client.put(self.set_detail_url, {
            "workout": self.workout_user1.id,
            "exercise": self.exercise.id,
            "reps": 15,
            "order": 1
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) # Check if the response status is 404 Not Found

        response = self.client.delete(self.set_detail_url) # Attempt to delete user1's set
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) # Check if the response status is 404 Not Found