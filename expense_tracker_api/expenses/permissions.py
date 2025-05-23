from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS are GET, HEAD, OPTIONS — allow these for anyone authenticated
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Otherwise, write permissions are only allowed to the object's owner
        return obj.user == request.user