
from rest_framework import permissions, viewsets, generics
from . models import ShortURL, ClickEvent
from . serializers import ShortURLSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from . permissions import IsOwnerOrReadOnly



class ShortURLViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling ShortURL objects.
    Provides CRUD operations for ShortURL objects.
    """
    queryset = ShortURL.objects.all()  # retrieve all ShortURL objects
    serializer_class = ShortURLSerializer  # serialization and deserialization of ShortURL objects
    permission_classes = [permissions.AllowAny, IsOwnerOrReadOnly]  # Allow any user to access this viewset
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user if self.request.user.is_authenticated else None)  # Save the user if authenticated, otherwise None


class RedirectToOriginalView(APIView):
    """"
    APIView to handle redirection from short code to original URL.
    """
    def get(self, request, short_code): # Handle GET requests to redirect to the original URL
        url_obj = get_object_or_404(ShortURL, short_code=short_code, is_active=True)  # Retrieve the ShortURL object by short_code

        # check if the URL has expired
        if url_obj.expiration_date and url_obj.expiration_date < timezone.now():
            return Response({'detail': 'URL has expired.'}, status=status.HTTP_410_GONE)
        
        # log the click event
        url_obj.clicks += 1 # Increment the click count
        url_obj.save() # Save the updated ShortURL object
        ClickEvent.objects.create(
            short_url=url_obj,  # Create a ClickEvent object with the ShortURL object
            ip_address=request.META.get('REMOTE_ADDR', ''),  # Get the user's IP address
            user_agent=request.META.get('HTTP_USER_AGENT', '')  # Get the user's user agent
        )
        return redirect(url_obj.original_url) # Redirect to the original URL
    

class ListUserURLsView(generics.ListAPIView):
    """
    APIView to list all ShortURL objects created by the authenticated user.
    """
    serializer_class = ShortURLSerializer  # Use the ShortURLSerializer for serialization
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access this view
    filter_backends = [DjangoFilterBackend] # Enable filtering on the queryset 
    filterset_fields = ['created_at', 'is_active', 'expiration_date'] # Fields that can be filtered in the queryset
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        return ShortURL.objects.filter(user=self.request.user)  # Return ShortURL objects created by the authenticated user

