from rest_framework import serializers
from .models import ShortURL
from urllib.parse import urlparse
import qrcode
import base64
from io import BytesIO
from rest_framework.validators import UniqueValidator
from django.utils import timezone

class ShortURLSerializer(serializers.ModelSerializer):
    short_code = serializers.CharField(
        required=False,
        validators=[
            UniqueValidator(queryset=ShortURL.objects.all(), message="This short code is already in use. Please choose a different one.")
        ]
    )  # Allow custom short codes, but ensure they are unique
    clicks = serializers.ReadOnlyField()  # Make clicks read-only since it's managed by the application
    created_at = serializers.ReadOnlyField()  # Make created_at read-only since it's set automatically

    # for generating a  QR code
    short_link = serializers.SerializerMethodField()  # Custom field to generate the short link
    qr_code = serializers.SerializerMethodField() # Custom field to generate QR code

    class Meta:
        model = ShortURL # Define the model to serialize
        fields = ['id', 'user', 'original_url', 'short_code','short_link', 'clicks', 'created_at', 'expiration_date', 'is_active', 'qr_code'] # Specify the fields to include in the serialized output, including qr_code

    def validate_original_url(self, value):
        """
        Validate that the original URL is a valid URL.
        """
        parsed = urlparse(value) # Parse the URL to check its validity
        if not parsed.scheme or not parsed.netloc: # Check if the URL has a valid scheme (http or https) and netloc (domain)
            raise serializers.ValidationError("Enter a valid URL with scheme (http:// or https://)")
        return value
    
    def get_short_link(self, obj):
        """
        Generate the short link for the URL.
        """
        request = self.context.get('request')
        path = f'/r/{obj.short_code}/'
        return request.build_absolute_uri(path) if request else path


    def get_qr_code(self, obj):
        """
        Generate a QR code for the short URL and return it as a base64-encoded string.
        """
        short_url = self.get_short_link(obj)
        qr = qrcode.make(short_url)  # Generate the QR code image
        buffer = BytesIO()  # Create a bytes buffer to hold the image
        qr.save(buffer, format='PNG')
        base64_qr = base64.b64encode(buffer.getvalue()).decode('utf-8')  # Encode the image to base64
        return f'data:image/png;base64,{base64_qr}'
    
    def validate_expiration_date(self, value):
        """
        Validate that the expiration date is in the future if provided
        """
        # if value is provided, check if it is in the past
        if value and value <= timezone.now():
            raise serializers.ValidationError("Expiration date must be in the future.") # raise an error then
        return value # return the value if valid
