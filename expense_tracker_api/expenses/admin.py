from django.contrib import admin
from .models import Transactions, Category

@admin.register(Category) # Register the Category model with the admin site
class CategoryAdmin(admin.ModelAdmin): 
    list_display = ('name', 'user', 'created_at') # Display these fields in the admin list view
    list_filter = ('user',) # Filter by user in the admin list view
    search_fields = ('name',) # Search by name in the admin list view

@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin): # Register the Transactions model with the admin site
    list_display = ('user', 'title', 'amount', 'type', 'category', 'created_at')
    list_filter = ('user', 'type', 'category', 'date') # Filter by user, type, category, and date in the admin list view
    search_fields = ('title', 'description')