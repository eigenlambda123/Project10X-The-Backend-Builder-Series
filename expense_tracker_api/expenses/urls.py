from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'transactions', views.TransactionsViewSet, basename='transactions')
# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),  # Include the router's URLs
]