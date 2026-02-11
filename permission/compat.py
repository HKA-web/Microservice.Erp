from django.conf import settings
from django.conf.urls import handler404, handler500, include
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group, Permission

__all__ = [
    'Group',
    'Permission',
    'AnonymousUser',
    'get_user_model',
    'user_model_label',
    'include',
    'handler404',
    'handler500',
]
user_model_label = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
def get_user_model_path():
    return getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

def get_user_permission_full_codename(perm):
    User = get_user_model()
    model_name = User._meta.model_name
    return '{}.{}_{}'.format(User._meta.app_label, perm, model_name)

def get_user_permission_codename(perm):
    return get_user_permission_full_codename(perm).split('.')[1]
