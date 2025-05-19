from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]