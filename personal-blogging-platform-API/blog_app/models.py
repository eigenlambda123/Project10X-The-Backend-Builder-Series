from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from markdown import markdown


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
    


class Post(models.Model):
    """
    Post model to represent a blog post.
    """
    title = models.CharField(max_length=200) # Field for post title
    slug = models.SlugField(max_length=200, unique=True, blank=True) # Slug field for URL-friendly representation
    content = models.TextField() # Field for post content
    html_content = models.TextField(blank=True) # Field for HTML content
    created_at = models.DateTimeField(auto_now_add=True) # Field for post creation date
    updated_at = models.DateTimeField(auto_now=True) # Field for post update date

    """
    ForeignKey relations
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE) # Foreign key to User model
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # Foreign key to Category model
    tags = models.ManyToManyField(Tag, blank=True) # Many-to-many relation to Tag model

    def save(self, *args, **kwargs):  
        if not self.slug:
            # Use slugify to create a URL-friendly slug from the title
            self.slug = slugify(self.title)
        # If html_content is empty, convert content to HTML
        if not self.html_content:
            # Convert the content to HTML using the markdown library
            self.html_content = markdown(self.content)
        # Call the parent class's save method
        super().save(*args, **kwargs)
    
    # String representation of the model
    # This will be used when we print the object
    def __str__(self):
        return self.title

