from django.apps import AppConfig
from django.core import management


class ApplicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
