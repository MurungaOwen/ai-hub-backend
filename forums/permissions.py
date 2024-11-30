from rest_framework import permissions

class IsPremiumUser(permissions.BasePermission):
    """
    Custom permission to allow only premium users to create threads.
    """

    def has_permission(self, request, view):
        # Allow safe methods (GET) for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_premium
