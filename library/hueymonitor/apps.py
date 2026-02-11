from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HueyMonitorConfig(AppConfig):
    name = 'hueymonitor'
    verbose_name = _('Huey Monitor')

    def ready(self) -> None:
        from . import checks
        if checks:
            pass
        from . import tasks
        if tasks:
            pass
        pass
