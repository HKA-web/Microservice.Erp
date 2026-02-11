from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ApplicationConfig(AppConfig):
    name = 'tasksonly'
    verbose_name = _('Tasks Only')

    def ready(self):
        from tasksonly import signals
        __all__ = [
            signals,
        ]
