import sys

from django.conf import settings as djangosettings

from permission.apps import ApplicationConfig

DEFAULTS = dict(
    SCHEMA=ApplicationConfig.name,
    ANONYMOUS_USER_NAME='AnonymousUser',
    RAISE_404=False,
    GET_INIT_ANONYMOUS_USER='permission.management.get_init_anonymous_user',
    MONKEY_PATCH=True,
    GET_CONTENT_TYPE='permission.content_types.get_default_content_type',
    AUTO_PREFETCH=False,
    USER_OBJECT_PERMS_MODEL='permission.UserObjectPermission',
    GROUP_OBJECT_PERMS_MODEL='permission.GroupObjectPermission',
)
__all__ = list(DEFAULTS)


def load():
    module = sys.modules[__name__]
    for name, default in DEFAULTS.items():
        setattr(module, name, getattr(djangosettings, ApplicationConfig.name.upper(), {}).get(name, default))


load()
