from .models import Transactions, Category
from django.contrib.auth.models import User
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault()) # Automatically set the user to the currently authenticated user

    class Meta:
        model = Category
        fields = ['id', 'name', 'user', 'slug', 'created_at'] # Fields to be serialized
        read_only_fields = ['user', 'slug', 'created_at'] # Fields that are read-only


class TransactionsSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault()) # Automatically set the user to the currently authenticated user
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all()) # Allow the user to select a category by its primary key
    category_detail = CategorySerializer(source='category', read_only=True) # Nested serializer to include category details


    class Meta:
        model = Transactions
        fields = ['id', 'user', 'category', 'title', 'description', 'type', 'amount', 'created_at', 'updated_at'] # Fields to be serialized
        read_only_fields = ['user', 'created_at', 'updated_at']

