import logging
import os
from itertools import chain

from django.conf import settings as djangosettings
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.contrib.auth.models import AnonymousUser, Group
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models import Model, QuerySet
from django.http import HttpResponseForbidden, HttpResponseNotFound

from permission import settings
from permission.content_types import get_content_type
from permission.exceptions import NotUserNorGroup

logger = logging.getLogger(__name__)
abspath = lambda *p: os.path.abspath(os.path.join(*p))


def get_anonymous_user():
    User = get_user_model()
    lookup = {User.USERNAME_FIELD: settings.ANONYMOUS_USER_NAME}
    return User.objects.get(**lookup)


def get_identity(identity):
    if isinstance(identity, AnonymousUser):
        identity = get_anonymous_user()
    if isinstance(identity, QuerySet):
        identity_model_type = identity.model
        if identity_model_type == get_user_model():
            return identity, None
        elif identity_model_type == Group:
            return None, identity
    if isinstance(identity, list) and isinstance(identity[0], get_user_model()):
        return identity, None
    if isinstance(identity, list) and isinstance(identity[0], Group):
        return None, identity
    if isinstance(identity, get_user_model()):
        return identity, None
    if isinstance(identity, Group):
        return None, identity
    raise NotUserNorGroup('User/AnonymousUser or Group instance is required (got %s)' % identity)


def get_error_or_None(request, perms, object=None, login_url=None, redirect_field_name=None, return_403=False, return_404=False, accept_global_perms=False, any_perm=False):
    login_url = login_url or djangosettings.LOGIN_URL
    redirect_field_name = redirect_field_name or REDIRECT_FIELD_NAME
    has_permissions = False
    if accept_global_perms:
        has_permissions = all(request.user.has_perm(perm) for perm in perms)
    if not has_permissions:
        if any_perm:
            has_permissions = any(request.user.has_perm(perm, object) for perm in perms)
        else:
            has_permissions = all(request.user.has_perm(perm, object) for perm in perms)
    if not has_permissions:
        if return_403:
            if settings.RAISE_403:
                raise PermissionDenied
            return HttpResponseForbidden()
        if return_404:
            if settings.RAISE_404:
                raise ObjectDoesNotExist
            return HttpResponseNotFound()
        else:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path(), login_url, redirect_field_name)


from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured


def get_object_perm_model_by_conf(setting_name):
    try:
        setting_value = getattr(settings, setting_name)
        return django_apps.get_model(setting_value, require_ready=False)
    except ValueError as e:
        raise ImproperlyConfigured('''{} must be of the form 'app_label.model_name' '''.format(setting_value)) from e
    except LookupError as e:
        raise ImproperlyConfigured('''{} refers to model '{}' that has not been installed'''.format(setting_name, setting_value)) from e


def clean_orphan_object_perms():
    UserObjectPermission = get_user_object_perms_model()
    GroupObjectPermission = get_group_object_perms_model()
    deleted = 0
    for perm in chain(UserObjectPermission.objects.all().iterator(), GroupObjectPermission.objects.all().iterator()):
        if perm.content_object is None:
            logger.debug('Removing %s (pk=%d)' % (perm, perm.pk))
            perm.delete()
            deleted += 1
    logger.info('Total removed orphan object permissions instances: %d' % deleted)
    return deleted


def get_object_perms_model(object, base_cls, generic_cls):
    if object is None:
        return generic_cls
    if isinstance(object, Model):
        object = object.__class__
    fields = (field for field in object._meta.get_fields() if (field.one_to_many or field.one_to_one) and field.auto_created)
    for attr in fields:
        model = getattr(attr, 'related_model', None)
        if (model and issubclass(model, base_cls) and
            model is not generic_cls and getattr(model, 'enabled', True)):
            if not model.objects.is_generic():
                fk = model._meta.get_field('content_object')
                if get_content_type(object) == get_content_type(fk.remote_field.model):
                    return model
    return generic_cls


def get_user_object_perms_model(object=None):
    from permission.models import UserObjectPermissionBase
    UserObjectPermission = get_object_perm_model_by_conf('USER_OBJECT_PERMS_MODEL')
    return get_object_perms_model(object, UserObjectPermissionBase, UserObjectPermission)


def get_group_object_perms_model(object=None):
    from permission.models import GroupObjectPermissionBase
    GroupObjectPermission = get_object_perm_model_by_conf('GROUP_OBJECT_PERMS_MODEL')
    return get_object_perms_model(object, GroupObjectPermissionBase, GroupObjectPermission)


def evict_object_perms_cache(object):
    if hasattr(object, '_permission_perms_cache'):
        delattr(object, '_permission_perms_cache')
        return True
    return False
