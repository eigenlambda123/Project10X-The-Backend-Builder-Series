import django_filters
from . models import Transactions

# Define a filter set for the Transactions model
class TransactionsFilter(django_filters.FilterSet):
    # Filter for transactions created on or after the given start_date
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    # Filter for transactions created on or before the given end_date
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        # Specify the model to filter
        model = Transactions
        # Allow filtering by category, start_date, and end_date
        fields = ['category', 'start_date', 'end_date']