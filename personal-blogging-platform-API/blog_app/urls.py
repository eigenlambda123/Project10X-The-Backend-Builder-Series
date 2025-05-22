from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, RegisterViewSet, PostDetailBySlugView, CategoryViewSet, TagViewSet

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    # path('posts/<slug:slug>/', PostDetailBySlugView.as_view(), name='post-detail-slug'),  # Post detail view by slug
    path('', include(router.urls)),
]

# Add the registration view to the urlpatterns
urlpatterns += [
    path('register/', RegisterViewSet.as_view(), name='register'),  # Registration view
]
