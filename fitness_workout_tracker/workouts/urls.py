from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import WorkoutViewSet

router = DefaultRouter()
router.register(r'workouts', WorkoutViewSet)

urlpatterns = [
    path('', include(router.urls)),
]