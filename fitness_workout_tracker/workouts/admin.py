from django.contrib import admin
from .models import Workout, Exercise, Set

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'date', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('date',)

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')

@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ('workout', 'exercise', 'reps', 'weight', 'order')
    list_filter = ('workout', 'exercise')
