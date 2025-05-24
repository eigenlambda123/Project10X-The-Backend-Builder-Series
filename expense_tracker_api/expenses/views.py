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
from rest_framework.decorators import action
from django.db.models import Sum
from datetime import datetime

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
    
    # Summary action to get the total income and expenses for the current user
    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request): 
        user = request.user # Get the current user
        queryset = self.get_queryset() # get the filtered queryset for the current user

        # Aggregate the total income and expenses for the current user
        total_income = queryset.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0.00 
        total_expense = queryset.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0.00
        net_balance = total_income - total_expense

        # return the summary data
        return Response({
            'total_income': total_income,
            'total_expense': total_expense,
            'net_balance': net_balance,
        })

    
