from django.contrib.auth import get_user_model
from workouts.views import WorkoutViewSet
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

User = get_user_model()

class WorkoutEndpointTests(TestCase):
    """
    Integration tests for the Workout API endpoints

    This test case covers the core CRUD operations for the Workout resource,
    including creation, retrieval (single and list), updating, deletion, and
    filtering by date. Each test simulates authenticated API requests using
    APIClient to ensure the endpoints behave as expected.
    """
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('workout-list') # dynamically resolve the URL for the WorkoutViewSet
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass') # create a dummy user for authentication
        self.client.force_authenticate(user=self.user) # authenticate the client with the test user
        self.test_workout_data = {
            "user": self.user.id,  
            "name": "Test Workout",
            "date": "2023-10-01",
            "notes": "This is a test workout."
        }

    def test_create_workout(self):
        """
        Test creating a workout via the API endpoint
        """

        # data 
        response = self.client.post(self.url, {
            "name": self.test_workout_data["name"],
            "date": self.test_workout_data["date"],
            "notes": self.test_workout_data["notes"],
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # check if status code is 201 CREATED

        # check if the response data matches the input data
        self.assertEqual(response.data['name'], self.test_workout_data['name'])
        self.assertEqual(response.data['notes'], self.test_workout_data['notes'])
        self.assertEqual(response.data['date'], self.test_workout_data['date'])
        self.assertEqual(response.data['user'], self.user.id) 


    def test_get_list_workouts(self):
        """
        Test retrieving the list of workouts via the API endpoint
        """
        # workout creation
        self.client.post(self.url, {
            "name": self.test_workout_data["name"],
            "date": self.test_workout_data["date"],
            "notes": self.test_workout_data["notes"],
        }, format='json')

        # get the list of workouts
        response = self.client.get(self.url, format='json') # send a GET request to the workouts endpoint

        self.assertEqual(response.status_code, status.HTTP_200_OK) # check if status code is 200 OK

    def test_get_single_workout(self):
        """
        Test retrieving a single workout via the API endpoint
        """

        # workout creation
        self.client.post(self.url, {
            "name": self.test_workout_data["name"],
            "date": self.test_workout_data["date"],
            "notes": self.test_workout_data["notes"],
        }, format='json')

        self.client.post(self.url, {
            "name": "Another Workout",
            "date": "2023-10-02",
            "notes": "This is another test workout."
        }, format='json')

        # get single workout via ID
        response = self.client.get(f"{self.url}2/", format='json') # get second workout by id 2
        self.assertEqual(response.status_code, status.HTTP_200_OK) # check if status code is 200 OK
        self.assertEqual(response.data['name'], "Another Workout") # check if the name matches


    def test_update_workout(self):
        """
        Test that updating a workout via the API endpoint Works
        """

        # workout creation
        self.client.post(self.url, {
            "name": self.test_workout_data["name"],
            "date": self.test_workout_data["date"],
            "notes": self.test_workout_data["notes"],
        }, format='json')

        # update the workout
        response = self.client.put(f"{self.url}1/", { 
            "name": "Updated Workout",
            "date": "2023-10-03",
            "notes": "This workout has been updated"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK) # check if status code is 200 OK
        self.assertEqual(response.data['name'], "Updated Workout") # check if the name is updated


    def test_delete_workout(self):
        """
        Test that deleting a workout via the API endpoint works
        """

        # workout creation
        self.client.post(self.url, {
            "name": self.test_workout_data["name"],
            "date": self.test_workout_data["date"],
            "notes": self.test_workout_data["notes"],
        }, format='json')

        # delete the workout 
        response = self.client.delete(f"{self.url}1/", format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) # check if status code is 204 NO CONTENT

    def test_filter_workouts_by_date(self):
        """
        Test filtering workouts by date via the API endpoint
        """
        # workout creation
        self.client.post(self.url, {
            "name": self.test_workout_data["name"],
            "date": self.test_workout_data["date"],
            "notes": self.test_workout_data["notes"],
        }, format='json')

        self.client.post(self.url, {
            "name": "Another Workout",
            "date": "2024-10-02",
            "notes": "This is another test workout."
        }, format='json')

        # filter workouts by date
        response = self.client.get(f"{self.url}?date={"2024-10-02"}", format='json') # filter by date 2024-10-02
        self.assertEqual(response.status_code, status.HTTP_200_OK) # check is status code is 200 OK
        self.assertEqual(len(response.data), 1) # check if only one workout is returned
        self.assertEqual(response.data[0]['name'], "Another Workout") # check if the name matches
        self.assertEqual(response.data['date'], "2024-10-02") # check if the date matches



class ExerciseEndpointTests(TestCase):
    """
    Integration tests for the Exercise API endpoints

    This test case covers the core CRUD operations for the Exercise resource,
    including creation, retrieval (single and list), updating, and deletion
    """
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('exercise-list') # dynamically resolve the URL for the ExerciseViewSet
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass') # create a dummy user for authentication
        self.client.force_authenticate(user=self.user) # authenticate the client with the test user
        self.test_exercise_data = {
            "name": "Test Exercise",
            "category": "push",
            "description": "This is a test exercise."
        }

    def test_create_exercise(self):
        """
        Test creating an exercise via the API endpoint
        """

        # create an exercise
        response = self.client.post(self.url, {
            "name": self.test_exercise_data["name"],
            "category": self.test_exercise_data["category"],
            "description": self.test_exercise_data["description"],
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # check if status code is 201 CREATED

    def test_get_list_exercises(self):
        """
        Test retrieving the list of exercises via the API endpoint
        """

        # create exercises
        self.client.post(self.url, {
            "name": self.test_exercise_data["name"],
            "category": self.test_exercise_data["category"],
            "description": self.test_exercise_data["description"],
        }, format='json')

        self.client.post(self.url, {
            "name": "Another Exercise",
            "category": "pull",
            "description": "This is another test exercise."
        }, format='json')

        # get the list of exercises
        response = self.client.get(self.url, format='json') # send a GET request to the exercises endpoint
        self.assertEqual(response.status_code, status.HTTP_200_OK) # check if status code is 200 OK
        self.assertEqual(len(response.data), 2) # check if two exercises are returned


    def test_get_single_exercise(self):
        """
        Test retrieving a single exercise via the API endpoint
        """

        # create exercises
        self.client.post(self.url, {
            "name": self.test_exercise_data["name"],
            "category": self.test_exercise_data["category"],
            "description": self.test_exercise_data["description"],
        }, format='json')

        self.client.post(self.url, {
            "name": "Another Exercise",
            "category": "pull",
            "description": "This is another test exercise."
        }, format='json')

        response = self.client.get(f"{self.url}2/", format='json') # get first exercise by id 2
        self.assertEqual(response.status_code, status.HTTP_200_OK) # check if status code is 200 OK
        self.assertEqual(response.data['name'], "Another Exercise") # check if the name matches

    def test_update_exercise(self):
        """
        Test that updating an exercise via the API endpoint works
        """

        # create an exercise
        self.client.post(self.url, {
            "name": self.test_exercise_data["name"],
            "category": self.test_exercise_data["category"],
            "description": self.test_exercise_data["description"],
        }, format='json')

        # update the exercise
        response = self.client.put(f"{self.url}1/", { 
            "name": "Updated Exercise",
            "category": "core",
            "description": "This exercise has been updated"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK) # check if status code is 200 OK

        # check if the datas are updated
        self.assertEqual(response.data['name'], "Updated Exercise") 
        self.assertEqual(response.data['category'], "core")
        self.assertEqual(response.data['description'], "This exercise has been updated")

    def test_delete_exercise(self):
        """
        Test that deleting an exercise via the API endpoint works
        """

        # create an exercise
        self.client.post(self.url, {
            "name": self.test_exercise_data["name"],
            "category": self.test_exercise_data["category"],
            "description": self.test_exercise_data["description"],
        }, format='json')

        
        response = self.client.delete(f"{self.url}1/", format='json') # delete the exercise 
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) # check if status code is 204 NO CONTENT


class SetEndpointTests(TestCase):
    """
    """

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('set-list') # dynamically resolve the URL for the SetViewSet
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass') # create a dummy user for authentication
        self.client.force_authenticate(user=self.user) # authenticate the client with the test user
        self.test_workout_data = {
            "user": self.user.id,  
            "workout": "Test Workout",
            "exercise": "Test Exercise",
            "reps": 10,
            "weight": 50.00,
            "duration": "00:30:00", 
            "notes": "This is a test set.",
        }
        
    def test_create_set(self):
        """
        Test creating a set via the API endpoint
        """

        # create a workout
        workout_response = self.client.post(reverse('workout-list'), {
            "name": "Test Workout",
            "date": "2023-10-01",
            "notes": "This is a test workout."
        }, format='json')
    
        workout_id = workout_response.data['id']  # dynamically retrieve the workout ID


        # create an exercise
        exercise_response = self.client.post(reverse('exercise-list'), {
            "name": "Test Exercise",
            "category": "push",
            "description": "This is a test exercise."
        }, format='json')
        exercise_id = exercise_response.data['id']  # dynamically retrieve the exercise ID
    

        # create a set
        response = self.client.post(self.url, {
            "workout": workout_id,  # use the dynamically retrieved workout ID
            "exercise": exercise_id,  # use the dynamically retrieved exercise ID
            "reps": self.test_workout_data["reps"],
            "weight": self.test_workout_data["weight"],
            "duration": self.test_workout_data["duration"],
            "notes": self.test_workout_data["notes"],
            "order": 1 
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # check if status code is 201 CREATED
        self.assertEqual(float(response.data['weight']), self.test_workout_data['weight']) # check if the weight matches
        self.assertEqual(float(response.data['weight']), float(self.test_workout_data['weight'])) # check if the weight matches
        self.assertEqual(response.data['duration'], self.test_workout_data['duration']) # check if the duration matches
        self.assertEqual(response.data['notes'], self.test_workout_data['notes']) # check if the notes match