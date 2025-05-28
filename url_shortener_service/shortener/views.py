
from rest_framework import permissions, viewsets
from . models import ShortURL, ClickEvent
from . serializers import ShortURLSerializer


class ShortURLViewSet(viewsets.ModelViewSet):
    queryset = ShortURL.objects.all()  # retrieve all ShortURL objects
    serializer_class = ShortURLSerializer  # serialization and deserialization of ShortURL objects
    permission_classes = [permissions.AllowAny]  # Allow any user to access this viewset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user if self.request.user.is_authenticated else None)  # Save the user if authenticated, otherwise None


