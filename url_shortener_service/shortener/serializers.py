from rest_framework import serializers
from .models import ShortURL

class ShortURLSerializer(serializers.ModelSerializer):
    short_code = serializers.ReadOnlyField()  # Make short_code read-only since it's generated automatically
    clicks = serializers.ReadOnlyField()  # Make clicks read-only since it's managed by the application
    created_at = serializers.ReadOnlyField()  # Make created_at read-only since it's set automatically

    class Meta:
        model = ShortURL # Define the model to serialize
        fields = ['id', 'user', 'original_url', 'short_code', 'clicks', 'created_at', 'expiration_date', 'is_active'] # Specify the fields to include in the serialized output