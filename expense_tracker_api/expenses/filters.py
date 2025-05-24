import django_filters
from .models import Transactions



# Define a filter set for the Transactions model
class TransactionsFilter(django_filters.FilterSet):
    # search by description


    # filter by amount range
    min_amount = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    max_amount = django_filters.NumberFilter(field_name='amount', lookup_expr='lte')


    # Filter for transactions created on or after the given start_date
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    # Filter for transactions created on or before the given end_date
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        # Specify the model to filter
        model = Transactions
        # Allow filtering by category, start_date, and end_date
        fields = ['category', 'start_date', 'end_date']

    # Custom method to filter by description
    def filter_by_description(self, queryset, name, value):
        return queryset.filter(description__icontains=value)