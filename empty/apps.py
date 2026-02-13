import logging

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class ApplicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'empty' #change this
    verbose_name = _('Empty') #change this
    dependencies = [
        'authentication',
        'core',
    ]

    def ready(self):
        from core.utils import search
        from library.simplehistory.models import HistoricalChanges
        for model in [model for model in self.get_models() if HistoricalChanges.__name__.lower() not in (
            base.__name__.lower() for base in model.__bases__
        ) and not any(name in model.__name__.lower() for name in ['comment'])]:
            # search.register(model)
            pass
        pass
        # from checks import signals
        __all__ = [
            # signals,
        ]
