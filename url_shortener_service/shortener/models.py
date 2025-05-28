from django.db import models
from django.contrib.auth.models import User
import string
import random
from hashids import Hashids

# def generate_short_code(length=6):
#     """Generate a random short code of specified length."""
#     characters = string.ascii_letters + string.digits  # Characters to use in the short code
#     return ''.join(random.choice(characters) for _ in range(length))  # Generate the short code

hashids = Hashids(min_length=6)  # Initialize Hashids for generating short codes

class ShortURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Optional foreign key to User model
    original_url = models.URLField()  # Field to store the original URL
    short_code = models.CharField(max_length=10, unique=True, blank=True) # Field to store the generated short code
    clicks = models.IntegerField(default=0) # Field to count the number of clicks on the short URL
    created_at = models.DateTimeField(auto_now_add=True) # Field to store the creation timestamp
    expiration_date = models.DateTimeField(null=True, blank=True) # Optional field for URL expiration
    is_active = models.BooleanField(default=True) # Field to indicate if the short URL is active
    
    def save(self, *args, **kwargs):
        """Override the save method to generate a short code if not already set."""
        # If the object is new (no id), save it first to get an id
        if not self.id:
           super().save(*args, **kwargs)
        # If the short_code is not set, generate it using Hashids
        if not self.short_code:  
            self.short_code = hashids.encode(self.id)
            super().save(update_fields=['short_code'])
        # If the short_code is already set, just save the object
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.short_code} → {self.original_url}"
    

class ClickEvent(models.Model):
    short_url = models.ForeignKey(ShortURL, on_delete=models.CASCADE)  # Foreign key to ShortURL model
    clicked_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the URL was clicked
    ip_address = models.CharField(max_length=45)  # Field to store the IP address of the user who clicked the URL
    user_agent = models.CharField(max_length=255, null=True, blank=True)  # Optional field for user agent information

    def __str__(self):
        return f"Click on {self.short_url.short_code} at {self.clicked_at}"
 