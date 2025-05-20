import django_filters
from .models import Post

class PostFilter(django_filters.FilterSet):
    """
    Custom filter for the Post models Category and Tags.
    """
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='iexact')
    tags = django_filters.CharFilter(field_name='tags__name', lookup_expr='iexact')

    class Meta:
        model = Post
        fields = ['category', 'tags']