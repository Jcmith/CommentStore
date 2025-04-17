from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def admin_required(view_func):
    """
    Decorator to restrict access to views for just users with is_admin=True
    """
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and getattr(request.user, 'is_admin', False):
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return _wrapped_view

