from django.contrib import admin
from .models import ShortURL, ClickEvent

@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('short_code', 'original_url', 'clicks', 'created_at', 'is_active', 'expiration_date', 'user')
    search_fields = ('short_code', 'original_url')
    list_filter = ('is_active',)

@admin.register(ClickEvent)
class ClickEventAdmin(admin.ModelAdmin):
    list_display = ('short_url', 'clicked_at', 'ip_address')
    search_fields = ('short_url__short_code', 'ip_address')

