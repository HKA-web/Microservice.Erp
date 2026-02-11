from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from permission import monkey_patch_user, monkey_patch_group


class ApplicationConfig(AppConfig):
    name = 'permission'
    verbose_name = _('Object Permission')

    def ready(self):
        from permission import settings
        __all__ = [
        ]
        monkey_patch_group()
        if settings.MONKEY_PATCH:
            monkey_patch_user()
