from django.contrib.auth import get_user_model
from django.db import router
from django.db.models import signals
from django.utils import translation, timezone
from django.utils.module_loading import import_string

from permission import settings

__all__ = [
    get_user_model,
    signals,
    import_string,
    router,
    settings,
]


def get_init_anonymous_user(User):
    kwargs = dict(
        user_id='anonymous',
        user_name=settings.ANONYMOUS_USER_NAME,
        email='anonymous@erpro.local',
        is_staff=False,
        is_superuser=False,
        locale=translation.get_language(),
        enable=True,
        is_active=True,
        date_joined=timezone.now(),
        actived_date=timezone.now(),
    )
    anonymous = User(**kwargs)
    anonymous.set_unusable_password()
    return anonymous


def create_anonymous_user(sender, **kwargs):
    User = get_user_model()
    if not router.allow_migrate_model(kwargs['using'], User):
        return
    try:
        lookup = {
            User.USERNAME_FIELD: settings.ANONYMOUS_USER_NAME
        }
        User.objects.using(kwargs['using']).get(**lookup)
    except User.DoesNotExist:
        retrieve_anonymous_function = import_string(settings.GET_INIT_ANONYMOUS_USER)
        anonymous = retrieve_anonymous_function(User)
        anonymous.save(using=kwargs['using'])


if settings.ANONYMOUS_USER_NAME is not None:
    from django.apps import apps

    signals.post_migrate.connect(
        create_anonymous_user,
        sender=apps.get_app_config('permission'),
        dispatch_uid='permission.management.create_anonymous_user',
    )
