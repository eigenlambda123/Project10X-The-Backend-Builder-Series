from django.db import models
from django.contrib.auth.models import User
import string
import random

class ShortURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Optional foreign key to User model
    original_url = models.URLField()  # Field to store the original URL
    short_code = models.CharField(max_length=10, unique=True, blank=True) # Field to store the generated short code
    created_at = models.DateTimeField(auto_now_add=True) # Field to store the creation timestamp
    expiration_date = models.DateTimeField(null=True, blank=True) # Optional field for URL expiration
    is_active = models.BooleanField(default=True) # Field to indicate if the short URL is active
 