from django.shortcuts import render
from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer, RegisterSerializer
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly 
from .filters import PostFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework import generics


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