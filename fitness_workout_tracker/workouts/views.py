from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from . permissions import IsOwnerOrReadOnly
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied

from django_filters.rest_framework import DjangoFilterBackend

from .models import Workout, Set, Exercise, ProgressPhoto
from django.db.models import Max
from .serializers import (
    WorkoutSerializer,
    SetSerializer,
    ExerciseSerializer,
    RegisterSerializer,
    ProgressPhotoSerializer,
)

from datetime import timedelta
from django.utils.timezone import now

class RegisterView(CreateAPIView):
    """
    API endpoint for user registration.

    - This view allows new users to register by submitting their information
    - It uses the RegisterSerializer to validate and create a new User instance
    - No authentication is required to access this endpoint
    """
    queryset = User.objects.all() # get all user
    serializer_class = RegisterSerializer # use RegisterSerializer
    permission_classes = [AllowAny] 


class WorkoutViewSet(ModelViewSet):
    """
    API endpoint for viewing and editing Workout instances

    - Provides list, create, retrieve, update, and delete actions for workouts
    - Supports ordering, searching, and filtering by date, name, and notes
    - Workouts are ordered by most recent date by default
    """
    queryset = Workout.objects.all().order_by('-date') # Order workouts by date, most recent first
    serializer_class = WorkoutSerializer # serialize to convert model instances to JSON
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend] # Enable ordering, searching, and filtering
    filterset_fields = ['date'] # Allow filtering by date
    ordering_fields = ['date', 'created_at'] # Allow ordering by date and created_at
    search_fields = ['name', 'notes'] # Allow searching by name and notes
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly] # User should be Authenticated to access this view

    def perform_create(self, serializer):
        """
        Override to set the user automatically when creating a workout
        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        Only return workouts for the authenticated user
        """
        return Workout.objects.filter(user=self.request.user).order_by('-date')

class ExerciseViewSet(ModelViewSet):
    """
    API endpoint for viewing and editing Exercise instances

    Provides list, create, retrieve, update, and delete actions for exercises
    Exercises are ordered by their name by default
    """
    queryset = Exercise.objects.all().order_by('name') # order exercises by their name
    serializer_class = ExerciseSerializer # serialize to convert model instances to JSON
    permission_classes = [IsAuthenticated] # User should be Authenticated to access this view

class SetViewSet(ModelViewSet):
    """
    API endpoint for viewing and editing Set instances

    Provides list, create, retrieve, update, and delete actions for sets
    Sets are ordered by their 'order' field by default
    """
    queryset = Set.objects.all().order_by('order') # order sets by their order field
    serializer_class = SetSerializer # serialize to convert model instances to JSON
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly] # User should be Authenticated to access this view

    def perform_create(self, serializer):
        """
        Automatically set the workout for the set to the authenticated user's workout
        """
        workout = serializer.validated_data['workout']
        if workout.user != self.request.user:
            raise PermissionDenied("You can only create sets for your own workouts.")
        serializer.save()

    def get_queryset(self):
        """
        Only return sets for the authenticated user's workouts
        """
        return Set.objects.filter(workout__user=self.request.user).order_by('order')
    
    

class PersonalRecordsView(APIView):
    """
    API endpoint to retrieve personal records for the authenticated user

    - Returns the maximum weight lifted for each exercise performed by the user
    - The response is a list of exercises with their IDs, names, and the user's max weight for each
    - Only authenticated users can access their own records
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get max weight per exercise for this user
        records = (
            Set.objects
            .filter(workout__user=user) # filter to owner 
            .values('exercise__id', 'exercise__name') # display id and name
            .annotate(max_weight=Max('weight')) # get and display max weight
            .order_by('exercise__name') # order by name
        )

        return Response(records) # return annotated record response
    

class WorkoutStreakView(APIView):
    """
    API endpoint to retrieve workout streak statistics for the authenticated user.

    - Returns the user's longest streak (most consecutive days with a workout)
    - Returns the user's current streak (consecutive days up to today with a workout)
    - Only authenticated users can access their own streak data
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Get all unique workout dates for the user, ordered by date
        dates = (
            Workout.objects
            .filter(user=user)
            .values_list('date', flat=True)
            .distinct()
            .order_by('date')
        )

        # Convert to set of unique dates for quick lookup
        date_set = set(dates)

        longest_streak = 0
        current_streak = 0
        today = now().date()

        # Calculate the longest streak by checking consecutive days in the user's workout history
        for date in dates:
            streak = 1
            next_day = date + timedelta(days=1)
            while next_day in date_set:
                streak += 1
                next_day += timedelta(days=1)
            longest_streak = max(longest_streak, streak)

        # Calculate the current streak (consecutive days up to today)
        streak_day = today
        while streak_day in date_set:
            current_streak += 1
            streak_day -= timedelta(days=1)

        # Return the streak statistics as a JSON response
        return Response({
            "longest_streak": longest_streak,
            "current_streak": current_streak
        })
    

class ProgressPhotoViewSet(ModelViewSet):
    """
    API endpoint for viewing and editing ProgressPhoto instances.

    Provides list, create, retrieve, update, and delete actions for progress photos
    Progress photos are associated with workouts and can only be accessed by the user who created them.
    """
    queryset = ProgressPhoto.objects.all() # Get all progress photos
    serializer_class = ProgressPhotoSerializer # Serialize to convert model instances to JSON
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly] # User should be Authenticated to access this view

    def get_queryset(self):
        """
        Only return progress photos for the authenticated user's workouts.
        """
        return ProgressPhoto.objects.filter(workout__user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically set the workout for the progress photo to the authenticated user's workout
        """
        workout = serializer.validated_data['workout']
        if workout.user != self.request.user:
            raise PermissionDenied("You can only create progress photos for your own workouts.")
        serializer.save()