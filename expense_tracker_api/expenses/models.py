from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100) # Name of the category
    user = models.ForeignKey(User, on_delete=models.CASCADE) # User who created the category
    slug = models.SlugField(max_length=100, unique=True) # Slug for the category
    created_at = models.DateTimeField(auto_now_add=True) # Timestamp when the category was created

    class Meta:
        unique_together = ('name', 'user') # Ensure that the combination of name and user is unique
        ordering = ['name'] # Order categories by name

    # Create a slug from the name before saving
    def save(self, *args, **kwargs):
        if not self.slug: # Only create a slug if it doesn't already exist
            # Use slugify to create a URL-friendly slug from the name
            self.slug = slugify(self.name)
        super().save(*args, **kwargs) # Call the parent class's save method


    def __str__(self): # String representation of the category
        return self.name


class Transactions(models.Model):
    TRANSACTION_TYPE = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions') # User who created the transaction
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # Category of the transaction
    title = models.CharField(max_length=100) # Title of the transaction
    description = models.TextField(blank=True) # Description of the transaction
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPE) # Type of the transaction (income or expense)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True) # Timestamp when the transaction was created
    updated_at = models.DateTimeField(auto_now=True) # Timestamp when the transaction was last updated