from django.shortcuts import render
from . serializers import TransactionsSerializer, CategorySerializer
from . models import Transactions, Category
from . permissions import IsOwnerOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all() # Get all categories
    serializer_class = CategorySerializer # Use the CategorySerializer for serialization
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly] # Only authenticated users can access this view
    lookup_field = 'slug' # Use the slug field for lookups

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user) # Filter categories to only those owned by the current user
    
class TransactionsViewSet(ModelViewSet):
    queryset = Transactions.objects.all() # Get all transactions
    serializer_class = TransactionsSerializer # Use the TransactionsSerializer for serialization
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly] # Only authenticated users can access this view

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user) # Filter transactions to only those owned by the current user