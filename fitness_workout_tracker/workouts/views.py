from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from .models import Workout, Set, Exercise
from .serializers import WorkoutSerializer, SetSerializer, ExerciseSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


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

    def perform_create(self, serializer):
        """
        Override to set the user automatically when creating a workout
        """
        serializer.save(user=self.request.user)

class ExerciseViewSet(ModelViewSet):
    """
    API endpoint for viewing and editing Exercise instances

    Provides list, create, retrieve, update, and delete actions for exercises
    Exercises are ordered by their name by default
    """
    queryset = Exercise.objects.all().order_by('name') # order exercises by their name
    serializer_class = ExerciseSerializer # serialize to convert model instances to JSON

class SetViewSet(ModelViewSet):
    """
    API endpoint for viewing and editing Set instances

    Provides list, create, retrieve, update, and delete actions for sets
    Sets are ordered by their 'order' field by default
    """
    queryset = Set.objects.all().order_by('order') # order sets by their order field
    serializer_class = SetSerializer # serialize to convert model instances to JSON