from rest_framework import serializers
from .models import Category, Tag

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']  # Include the fields you want to serialize
        read_only_fields = ['id', 'slug'] # Specify which fields are read-only


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for the Tag model.
    """
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']  # Include the fields you want to serialize
        read_only_fields = ['id', 'slug'] # Specify which fields are read-only
        