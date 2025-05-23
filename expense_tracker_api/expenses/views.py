from django.shortcuts import render
from . serializers import TransactionsSerializer, CategorySerializer
from . models import Transactions, Category
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all() # Get all categories
    serializer_class = CategorySerializer # Use the CategorySerializer for serialization
    permission_classes = [IsAuthenticated] # Only authenticated users can access this view

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user) # Filter categories to only those owned by the current user
    
    