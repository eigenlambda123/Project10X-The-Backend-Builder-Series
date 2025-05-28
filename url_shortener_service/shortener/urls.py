from django.urls import path
from .views import ShortURLViewSet, RedirectToOriginalView, ListUserURLsView

urlpatterns = [
    path('api/shorten/', ShortURLViewSet.as_view(), name='shorten-url'),
    path('api/urls/', ListUserURLsView.as_view(), name='list-urls'),
    path('r/<str:short_code>/', RedirectToOriginalView.as_view(), name='redirect'),
]