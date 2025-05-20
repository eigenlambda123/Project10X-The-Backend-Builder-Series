from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, RegisterViewSet

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

# Add the registration view to the urlpatterns
urlpatterns += [
    path('api/register/', RegisterViewSet.as_view(), name='register'),  # Registration view
]
