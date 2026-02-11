import sys

from django.conf import settings as djangosettings

from report.apps import ApplicationConfig

DEFAULTS = dict(
    SCHEMA=ApplicationConfig.name,
    DEFAULT_FIELDS={},
)
__all__ = list(DEFAULTS)


def load():
    module = sys.modules[__name__]
    for name, default in DEFAULTS.items():
        setattr(module, name, getattr(djangosettings, ApplicationConfig.name.upper(), {}).get(name, default))


load()
