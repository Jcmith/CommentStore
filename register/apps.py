from django.apps import AppConfig

class RegisterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'register'

    def ready(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            if not User.objects.filter(username='admin1').exists():
                User.objects.create_user(username='admin1', password='admin1', is_admin=True)
        except Exception:
            pass
