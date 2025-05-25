from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Transactions, Category
from .serializers import TransactionsSerializer, CategorySerializer, RegisterSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import TransactionsFilter

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()  # Required by DRF to determine the model class; not used to list users
    serializer_class = RegisterSerializer  # Handles validation and creation of new users
    permission_classes = [AllowAny]  # Allows access to unauthenticated users (for public registration)

    def perform_create(self, serializer):
        serializer.save()  # Calls serializer.create() to save the new user instance


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

        # Monthly Filter
        month = request.query_params.get('month') # Get the month from query parameters
        if month:
            try:
                month_date = datetime.strptime(month, "%Y-%m")
                queryset = queryset.filter(
                    created_at__year=month_date.year,
                    created_at__month=month_date.month
                )
            except ValueError:
                return Response({"error": "Invalid month format. Use YYYY-MM."}, status=400)



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

    
