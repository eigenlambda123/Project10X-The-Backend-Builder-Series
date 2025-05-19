from django.shortcuts import render
from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
from .permissions import IsOwnerOrReadOnly 
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Post model.
    """
    queryset = Post.objects.all()  # Queryset to retrieve all posts
    serializer_class = PostSerializer  # Serializer class to use for serialization
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]  # Permissions for the viewset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # Save the post with the current user as the author
  