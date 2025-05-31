from rest_framework import serializers
from .models import Category, Tag, Post
import markdown
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User # User model from Django's auth system
        fields = ['username', 'email', 'password'] # Fields to be serialized
        extra_kwargs = {
            'password': {'write_only': True} # Password should be write-only
        }

    # Override the create method to handle user creation
    # and password hashing
    def create(self, validated_data):
        """
        Create a new user with the provided validated data.
        """
        # Create a new user instance with the provided username and email
        user = User(
            username=validated_data['username'], # Set the username field
            email=validated_data['email'] # Set the email field
        )
        user.set_password(validated_data['password']) # Hash the password
        user.save() # Save the user instance to the database
        return user # Return the created user instance

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
        

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.
    """

    # Use SlugRelatedField to represent the category by its 'name' field.
    # Allows assigning a category by name when creating/updating a post.
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='name',
    )

    # Use SlugRelatedField for tags, representing each tag by its 'name'.
    # Supports multiple tags (many-to-many relationship).
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        slug_field='name',
        many=True,  # for many-to-many relationship
    )
    html_content = serializers.SerializerMethodField()  # Custom field for HTML content

    # Explicitly define author as read-only
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'html_content', 'created_at', 'updated_at', 'category','author', 'tags']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']

    def get_html_content(self, obj):
        """
        Convert the raw Markdown content of a Post into HTML
        when serializing it in the API response
        """
        return markdown.markdown(obj.content)
        
    
    def create(self, validated_data):
        """
        Override create method to set author to the authenticated user.
        """
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)