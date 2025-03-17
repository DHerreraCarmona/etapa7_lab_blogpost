from django.apps import AppConfig
from django.db.models.signals import post_migrate


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.user'

    def ready(self):
        from .signals import create_roles  # Import your signal function
        post_migrate.connect(create_roles, sender=self)