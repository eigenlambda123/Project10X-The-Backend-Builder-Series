from django.db import models
from django.contrib.auth.models import User

class Workout(models.Model):
    """
    Model representing a workout session for a user
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Link to user who the workout belongs to
    name = models.CharField(max_length=100) # name of workout
    date = models.DateField() # date of workout
    notes = models.TextField(blank=True, optional=True) # additional notes about the workout
    created_at = models.DateTimeField(auto_now_add=True) # when the workout was created
    updated_at = models.DateTimeField(auto_now=True) # when the workout was last updated

    def __str__(self):
        """
        String representation of the Workout model
        """
        return f"{self.name} - {self.user.username} ({self.date})"
    
