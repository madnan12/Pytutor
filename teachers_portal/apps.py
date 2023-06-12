from django.apps import AppConfig


class TeachersPortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'teachers_portal'

    def ready(self):
        from . import signals
