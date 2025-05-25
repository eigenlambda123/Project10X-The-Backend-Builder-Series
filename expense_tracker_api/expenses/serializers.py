from .models import Transactions, Category
from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password field that is write-only

    class Meta:
        model = User # User model to be serialized
        fields = ['username', 'email', 'password'] # Fields to be serialized

    # Create a new user instance with the validated data
    def create(self, validated_data):
        # Create a new user with the provided username, email, and password
        if User.objects.filter(username=validated_data['username']).exists(): # Check if the username already exists
            raise serializers.ValidationError({"username": "Username already exists."})
        # If the username is unique, create the user
        user = User.objects.create_user( 
            username=validated_data['username'], 
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault()) # Automatically set the user to the currently authenticated user

    class Meta:
        model = Category
        fields = ['id', 'name', 'user', 'slug', 'created_at'] # Fields to be serialized
        read_only_fields = ['user', 'slug', 'created_at'] # Fields that are read-only


class TransactionsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault()) # Automatically set the user to the currently authenticated user
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all()) # Allow the user to select a category by its primary key
    # category_detail = CategorySerializer(source='category', read_only=True) # Nested serializer to include category details

    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user # Get the current user from the request context
        # If the user is authenticated, filter the categories to only those owned by the user
        if user.is_authenticated:
            self.fields['category'].queryset = Category.objects.filter(user=user)  # Limit categories to those owned by the current user


    class Meta:
        model = Transactions
        fields = ['id', 'user', 'category', 'title', 'description', 'type', 'amount', 'created_at', 'updated_at'] # Fields to be serialized
        read_only_fields = ['user', 'created_at', 'updated_at']

