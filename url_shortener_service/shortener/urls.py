from django.urls import path
from .views import ShortURLViewSet, RedirectToOriginalView, ListUserURLsView

from rest_framework.routers import DefaultRouter
from shortener.views import ShortURLViewSet

router = DefaultRouter()
router.register(r'api/shorten', ShortURLViewSet, basename='shorturl')

urlpatterns = [
    path('api/user-urls/', ListUserURLsView.as_view(), name='user_urls'), 
    path('r/<str:short_code>/', RedirectToOriginalView.as_view(), name='redirect'),
]

urlpatterns += router.urls  
