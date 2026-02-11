from collections.abc import Iterable

from django.conf import settings as djangosettings
from django.contrib.auth.decorators import login_required, REDIRECT_FIELD_NAME
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from permission.utils import get_user_object_perms_model

UserObjectPermission = get_user_object_perms_model()
from permission.utils import get_error_or_None, get_anonymous_user
from permission.shortcuts import get_objects_for_user


class LoginRequiredMixin:
    redirect_field_name = REDIRECT_FIELD_NAME
    login_url = djangosettings.LOGIN_URL

    def dispatch(self, request, *args, **kwargs):
        return login_required(redirect_field_name=self.redirect_field_name, login_url=self.login_url)(super().dispatch)(request, *args, **kwargs)


class PermissionRequiredMixin:
    login_url = djangosettings.LOGIN_URL
    permission_required = None
    redirect_field_name = REDIRECT_FIELD_NAME
    return_403 = False
    return_404 = False
    raise_exception = False
    accept_global_perms = False
    any_perm = False

    def get_required_permissions(self, request=None):
        if isinstance(self.permission_required, str):
            perms = [self.permission_required]
        elif isinstance(self.permission_required, Iterable):
            perms = [p for p in self.permission_required]
        else:
            raise ImproperlyConfigured(''''PermissionRequiredMixin' requires 'permission_required' attribute to be set to '<app_label>.<permission codename>' but is set to '%s' instead''' % self.permission_required)
        return perms

    def get_permission_object(self):
        if hasattr(self, 'permission_object'):
            return self.permission_object
        return (hasattr(self, 'get_object') and self.get_object() or
                getattr(self, 'object', None))

    def check_permissions(self, request):
        object = self.get_permission_object()
        forbidden = get_error_or_None(
            request,
            perms=self.get_required_permissions(request),
            object=object,
            login_url=self.login_url,
            redirect_field_name=self.redirect_field_name,
            return_403=self.return_403,
            return_404=self.return_404,
            accept_global_perms=self.accept_global_perms,
            any_perm=self.any_perm,
        )
        if forbidden:
            self.on_permission_check_fail(request, forbidden, object=object)
        if forbidden and self.raise_exception:
            raise PermissionDenied()
        return forbidden

    def on_permission_check_fail(self, request, response, object=None):

        def dispatch(self, request, *args, **kwargs):
            self.request = request
            self.args = args
            self.kwargs = kwargs
            response = self.check_permissions(request)
            if response:
                return response
            return super().dispatch(request, *args, **kwargs)


class PermissionUserMixin:
    @staticmethod
    def get_anonymous():
        return get_anonymous_user()

    def add_object_perm(self, perm, object):
        return UserObjectPermission.objects.assign_perm(perm, self, object)

    def del_object_perm(self, perm, object):
        return UserObjectPermission.objects.remove_perm(perm, self, object)


class PermissionListMixin:
    permission_required = None
    get_objects_for_user_extra_kwargs = {}

    def get_required_permissions(self, request=None):
        if isinstance(self.permission_required, str):
            perms = [self.permission_required]
        elif isinstance(self.permission_required, Iterable):
            perms = [p for p in self.permission_required]
        else:
            raise ImproperlyConfigured(''''PermissionRequiredMixin' requires 'permission_required' attribute to be set to '<app_label>.<permission codename>' but is set to '%s' instead''' % self.permission_required)
        return perms

    def get_get_objects_for_user_kwargs(self, queryset):
        return dict(
            user=self.request.user,
            perms=self.get_required_permissions(self.request),
            klass=queryset,
            **self.get_objects_for_user_extra_kwargs
        )

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return get_objects_for_user(**self.get_get_objects_for_user_kwargs(queryset))
