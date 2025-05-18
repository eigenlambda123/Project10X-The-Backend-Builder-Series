from django.db import models
from django.utils.text import slugify

# Create Category model
class Category(models.Model):
    """
    Category model to categorize blog posts.
    """
    name = models.CharField(max_length=100, unique=True) # Field for category name
    slug = models.SlugField(max_length=100, unique=True, blank=True) # Slug field for URL-friendly representation

    # Create a slug from the name before saving
    def save(self, *args, **kwargs):
        if not self.slug: # Only create a slug if it doesn't already exist
            # Use slugify to create a URL-friendly slug from the name
            self.slug = slugify(self.name)
        super().save(*args, **kwargs) # Call the parent class's save method

    # String representation of the model
    # This will be used when we print the object
    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Tag model to tag blog posts.
    """
    name = models.CharField(max_length=100, unique=True) # Field for tag name
    slug = models.SlugField(max_length=100, unique=True, blank=True) # Slug field for URL-friendly representation

    def save(self, *args, **kwargs):
        if not self.slug:
            # Use slugify to create a URL-friendly slug from the name
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    # String representation of the model
    def __str__(self):
        return self.name
