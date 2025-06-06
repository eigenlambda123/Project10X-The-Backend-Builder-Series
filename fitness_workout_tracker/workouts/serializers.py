from rest_framework.serializers import ModelSerializer
from .models import Workout, Exercise, Set

class WorkoutSerializer(ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'user', 'name', 'date', 'notes', 'created_at', 'updated_at']

class ExerciseSerializer(ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'category', 'name', 'description']

class SetSerializer(ModelSerializer):
    class Meta:
        model = Set
        fields = ['id', 'workout', 'exercise', 'reps', 'weight', 'duration', 'notes', 'created_at', 'updated_at', 'order']