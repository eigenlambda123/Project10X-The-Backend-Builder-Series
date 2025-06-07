from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from .models import Workout
from .serializers import WorkoutSerializer
from rest_framework import filters


class WorkoutViewSet(ModelViewSet):
    """
    API endpoint for viewing and editing Workout instances

    - Provides list, create, retrieve, update, and delete actions for workouts
    - Supports ordering, searching, and filtering by date, name, and notes
    - Workouts are ordered by most recent date by default
    """
    queryset = Workout.objects.all().order_by('-date') # Order workouts by date, most recent first
    serializer_class = WorkoutSerializer # serialize to convert model instances to JSON
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, filters.DjangoFilterBackend] # Enable ordering, searching, and filtering
    filterset_fields = ['date'] # Allow filtering by date
    ordering_fields = ['date', 'created_at'] # Allow ordering by date and created_at
    search_fields = ['name', 'notes'] # Allow searching by name and notes