from django.contrib.auth.decorators import user_passes_test


# Custom admin flag to restrict views
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.is_admin)(view_func)