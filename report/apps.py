from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ApplicationConfig(AppConfig):
    name = 'report'
    verbose_name = _('Report')
    dependencies = [
        'core',
    ]

    def ready(self):
        __all__ = [
        ]
