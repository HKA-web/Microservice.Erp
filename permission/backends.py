from django.contrib.auth import get_user_model
from django.db import models

from permission import settings
from permission.core import ObjectPermissionChecker
from permission.content_types import get_content_type
from permission.exceptions import WrongAppError


def check_object_support(object):
    return isinstance(object, models.Model)


def check_user_support(user_object):
    if not user_object.is_authenticated:
        if settings.ANONYMOUS_USER_NAME is None:
            return False, user_object
        User = get_user_model()
        lookup = {
            User.USERNAME_FIELD: settings.ANONYMOUS_USER_NAME
        }
        user_object = User.objects.get(**lookup)
    return True, user_object


def check_support(user_object, object):
    object_support = check_object_support(object)
    user_support, user_object = check_user_support(user_object)
    return object_support and user_support, user_object


class ObjectPermissionBackend:
    supports_object_permissions = True
    supports_anonymous_user = True
    supports_inactive_user = True

    def authenticate(self, request, username=None, password=None):
        return None

    def has_perm(self, user_object, perm, object=None):
        support, user_object = check_support(user_object, object)
        if not support:
            return False
        if '.' in perm:
            app_label, _ = perm.split('.', 1)
            if app_label != object._meta.app_label:
                ctype = get_content_type(object)
                if app_label != ctype.app_label:
                    raise WrongAppError('''Passed perm has app label of '%s' while given obj has app label '%s' and given obj content_type has app label '%s' ''' % (app_label, object._meta.app_label, ctype.app_label))

        check = ObjectPermissionChecker(user_object)
        return check.has_perm(perm, object)

    def get_all_permissions(self, user_object, object=None):
        support, user_object = check_support(user_object, object)
        if not support:
            return set()

        check = ObjectPermissionChecker(user_object)
        return check.get_perms(object)
