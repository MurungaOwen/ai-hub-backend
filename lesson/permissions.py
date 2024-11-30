from rest_framework.permissions import BasePermission
from django.utils import timezone

class IsPremiumUser(BasePermission):
    """
    Custom permission to only allow access to premium users.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_premium and request.user.premium_expiry > timezone.now()
