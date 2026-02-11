from django.apps import apps
from django.conf import settings as djangosettings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.db.models import Model
from django.db.models.base import ModelBase
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.utils.functional import wraps

from permission.exceptions import PermissionError
from permission.utils import get_error_or_None


def permission_required(perm, lookup_variables=None, **kwargs):
    login_url = kwargs.pop('login_url', djangosettings.LOGIN_URL)
    redirect_field_name = kwargs.pop('redirect_field_name', REDIRECT_FIELD_NAME)
    return_403 = kwargs.pop('return_403', False)
    return_404 = kwargs.pop('return_404', False)
    accept_global_perms = kwargs.pop('accept_global_perms', False)
    if not isinstance(perm, str):
        raise PermissionError('''First argument must be in format: 'app_label.codename or a callable which return similar string' ''')

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            object = None
            if lookup_variables:
                model, lookups = lookup_variables[0], lookup_variables[1:]
                if isinstance(model, str):
                    splitted = model.split('.')
                    if len(splitted) != 2:
                        raise PermissionError('''If model should be looked up from string it needs format: 'app_label.ModelClass' ''')
                    model = apps.get_model(*splitted)
                elif issubclass(model.__class__, (Model, ModelBase, QuerySet)):
                    pass
                else:
                    raise PermissionError('''First lookup argument must always be a model, string pointing at app/model or queryset. Given: %s (type: %s)''' % (model, type(model)))
                if len(lookups) % 2 != 0:
                    raise PermissionError('Lookup variables must be provided as pairs of lookup string and viewarg')
                lookupdict = {}
                for lookup, viewarg in zip(lookups[::2], lookups[1::2]):
                    if viewarg not in kwargs:
                        raise PermissionError('Argument %s was not passed into view function' % viewarg)
                    lookupdict[lookup] = kwargs[viewarg]
                object = get_object_or_404(model, **lookupdict)
            response = get_error_or_None(request, perms=[perm], object=object, login_url=login_url, redirect_field_name=redirect_field_name, return_403=return_403, return_404=return_404, accept_global_perms=accept_global_perms)
            if response:
                return response
            return view_func(request, *args, **kwargs)

        return wraps(view_func)(_wrapped_view)

    return decorator


def permission_required_or_403(perm, *args, **kwargs):
    kwargs['return_403'] = True
    return permission_required(perm, *args, **kwargs)


def permission_required_or_404(perm, *args, **kwargs):
    kwargs['return_404'] = True
    return permission_required(perm, *args, **kwargs)
