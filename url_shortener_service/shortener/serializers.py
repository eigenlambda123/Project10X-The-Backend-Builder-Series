from rest_framework import serializers
from .models import ShortURL
from urllib.parse import urlparse

class ShortURLSerializer(serializers.ModelSerializer):
    short_code = serializers.ReadOnlyField()  # Make short_code read-only since it's generated automatically
    clicks = serializers.ReadOnlyField()  # Make clicks read-only since it's managed by the application
    created_at = serializers.ReadOnlyField()  # Make created_at read-only since it's set automatically

    class Meta:
        model = ShortURL # Define the model to serialize
        fields = ['id', 'user', 'original_url', 'short_code', 'clicks', 'created_at', 'expiration_date', 'is_active'] # Specify the fields to include in the serialized output

    def validate_original_url(self, value):
        """
        Validate that the original URL is a valid URL.
        """
        parsed = urlparse(value) # Parse the URL to check its validity
        if not parsed.scheme or not parsed.netloc: # Check if the URL has a valid scheme (http or https) and netloc (domain)
            raise serializers.ValidationError("Enter a valid URL with scheme (http:// or https://)")
        return value