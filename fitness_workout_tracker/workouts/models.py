from django.db import models
from django.contrib.auth.models import User

class Workout(models.Model):
    """
    Model representing a workout session for a user
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Link to user who the workout belongs to
    name = models.CharField(max_length=100) # name of workout
    date = models.DateField() # date of workout
    notes = models.TextField(blank=True, null=True) # additional notes about the workout
    created_at = models.DateTimeField(auto_now_add=True) # when the workout was created
    updated_at = models.DateTimeField(auto_now=True) # when the workout was last updated

    def __str__(self):
        """
        returns the name of the workout, username, and date of the workout
        """
        return f"{self.name} - {self.user.username} ({self.date})"
    

class Exercise(models.Model):
    """
    Catalog of exercise types
    """
    name = models.CharField(max_length=100) # name of the exercise
    description = models.TextField(blank=True, null=True) # description of the exercise, optional
    
    def __str__(self):
        """
        returns the name of the exercise"""
        return self.name
    
class Set(models.Model):
    """
    Model representing a set within an exercise
    """
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='sets') # Link to the workout this set belongs to
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE) # Link to the exercise this set belongs to
    reps = models.PositiveIntegerField() # number of reps for this set
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True) # weight used for this set, optional
    duration = models.DurationField(blank=True, null=True) # duration of the set, optional
    notes = models.TextField(blank=True, null=True) # additional notes about the set
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        returns the exercise name, reps, and weight for the set
        """
        return f"{self.exercise.name}: {self.reps} reps @ {self.weight} lbs"

    
