from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Workout, Exercise, Set

class SetSerializer(ModelSerializer):
    exercise_name = serializers.ReadOnlyField(source='exercise.name') # This will return the name of the exercise in the serialized output

    class Meta:
        model = Set
        fields = ['id', 'workout', 'exercise' ,'exercise_name', 'reps', 'weight', 'duration', 'notes', 'created_at', 'updated_at', 'order']
        read_only_fields = ['id','created_at', 'updated_at']

class WorkoutSerializer(ModelSerializer):
    sets = SetSerializer(many=True, read_only=True) # This will include the sets in the workout serialization

    class Meta:
        model = Workout
        fields = ['id', 'user', 'name', 'date', 'notes', 'sets', 'created_at', 'updated_at']
        read_only_fields = ['id','created_at', 'updated_at', 'user']

class ExerciseSerializer(ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'category', 'name', 'description']

