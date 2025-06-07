from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import WorkoutViewSet, SetViewSet

router = DefaultRouter()
router.register(r'workouts', WorkoutViewSet)
router.register(r'sets', SetViewSet, basename='set')

urlpatterns = [
    path('', include(router.urls)),
]