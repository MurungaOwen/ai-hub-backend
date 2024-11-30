from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.utils import timezone


def premium_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_premium and request.user.premium_expiry > timezone.now():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You must have a premium account to access this content.")
    return _wrapped_view
