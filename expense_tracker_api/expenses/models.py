from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100) # Name of the category
    user = models.ForeignKey(User, on_delete=models.CASCADE) # User who created the category
    slug = models.SlugField(max_length=100, unique=True) # Slug for the category

    class Meta:
        unique_together = ('name', 'user') # Ensure that the combination of name and user is unique
        ordering = ['name'] # Order categories by name

    def __str__(self): # String representation of the category
        self.name

