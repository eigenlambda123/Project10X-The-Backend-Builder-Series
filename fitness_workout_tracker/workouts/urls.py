from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import WorkoutViewSet, SetViewSet, ExerciseViewSet

router = DefaultRouter()
router.register(r'workouts', WorkoutViewSet)
router.register(r'exercises', ExerciseViewSet, basename='exercise')
router.register(r'sets', SetViewSet, basename='set')

urlpatterns = [
    path('', include(router.urls)),
]