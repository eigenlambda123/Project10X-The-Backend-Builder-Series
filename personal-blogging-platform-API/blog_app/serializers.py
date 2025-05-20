from rest_framework import serializers
from .models import Category, Tag, Post
from markdown import markdown

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


    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'html_content', 'created_at', 'updated_at', 'category', 'tags']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']

    def get_html_content(self, obj):
        """
        Convert the raw Markdown content of a Post into HTML
        when serializing it in the API response
        """
        return markdown(obj.content)
        