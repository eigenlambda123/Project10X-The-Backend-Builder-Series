from django.contrib import admin
from .models import Post, Category, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin interface for the Post model.
    """
    list_display = ('title', 'author', 'category', 'created_at')
    prepopulated_fields = {'slug': ('title',)}  # Automatically populate the slug field based on the title

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for the Category model.
    """
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = "Category"
    verbose_name_plural = "Category"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin interface for the Tag model.
    """
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}