from .models import Transactions, Category
from django.contrib.auth.models import User
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'user', 'slug', 'created_at'] # Fields to be serialized
        read_only_fields = ['user', 'slug', 'created_at'] # Fields that are read-only


class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ['id', 'user', 'category', 'title', 'description', 'type', 'amount', 'created_at', 'updated_at'] # Fields to be serialized
        read_only_fields = ['user', 'created_at', 'updated_at']

