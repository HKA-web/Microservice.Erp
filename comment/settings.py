import logging
import sys

from django.conf import settings as djangosettings

from comment.apps import ApplicationConfig

logger = logging.getLogger(__name__)

DEFAULTS = dict(
    SCHEMA = ApplicationConfig.name,
)
__all__ = list(DEFAULTS)


def load():
    module = sys.modules[__name__]
    for name, default in DEFAULTS.items():
        setattr(module, name, getattr(djangosettings, ApplicationConfig.name.upper(), {}).get(name, default))


load()
