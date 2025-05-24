from django.shortcuts import render
from . serializers import TransactionsSerializer, CategorySerializer
from . models import Transactions, Category
from . permissions import IsOwnerOrReadOnly
from . filters import TransactionsFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Q

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
    filter_backends = [DjangoFilterBackend] # Use DjangoFilterBackend for filtering
    filterset_class = TransactionsFilter # Use the TransactionsFilter for filtering

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user) # Filter transactions to only those owned by the current user
    
# SummaryView to get the total income, expenses, and profit for the authenticated user
class SummaryView(APIView):
    permission_classes = [IsAuthenticated] # Only authenticated users can access this view

    def get(self, request):
        user = request.user
        Transactions = Transactions.objects.filter(user=user) # Get all transactions for the authenticated user

        # Calculate total income, expenses, and profit
        total_income = Transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = Transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        net_balance = total_income - total_expense

        