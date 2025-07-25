from django.shortcuts import render
from rest_framework import viewsets
from .models import Post, Category, Tag
from .serializers import PostSerializer, RegisterSerializer, CategorySerializer, TagSerializer
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly 
from .filters import PostFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining JWT token pairs.

    This view uses the custom MyTokenObtainPairSerializer to include the username
    in the JWT payload when a user logs in. By overriding the default serializer,
    the frontend can access the username directly from the token without making
    an additional API call.
    """
    serializer_class = MyTokenObtainPairSerializer


class RegisterViewSet(generics.CreateAPIView):
    """
    ViewSet for user registration
    """
    queryset = User.objects.all()  # Queryset to retrieve all users
    serializer_class = RegisterSerializer  # Serializer class to use for serialization
    permission_classes = [AllowAny]  # Permissions for the viewset


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Post model.
    """
    queryset = Post.objects.all().order_by('-created_at')  # queryset to retrieve all posts, ordered by creation date
    serializer_class = PostSerializer  # Serializer class to use for serialization
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]  # Permissions for the viewset
    filter_backends = [DjangoFilterBackend]  # Filter backend for filtering posts
    filterset_class = PostFilter # Fields to filter by
    lookup_field = 'slug'  # Use the slug field for lookups

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # Save the post with the current user as the author
  

class PostDetailBySlugView(generics.RetrieveUpdateDestroyAPIView):
    """
    ViewSet for retrieving, updating, and deleting a post by its slug.
    """
    queryset = Post.objects.all()  # Queryset to retrieve all posts
    serializer_class = PostSerializer  # Serializer class to use for serialization
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]  # Permissions for the viewset


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Category model.
    """
    queryset = Category.objects.all()  # Queryset to retrieve all posts
    serializer_class = CategorySerializer  # Serializer class to use for serialization


class TagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Tag model.
    """
    queryset = Tag.objects.all()  # Queryset to retrieve all posts
    serializer_class = TagSerializer  # Serializer class to use for serialization
