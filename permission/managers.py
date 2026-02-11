from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.db.models import Q
from permission.core import ObjectPermissionChecker
from permission.content_types import get_content_type
from permission.exceptions import ObjectNotPersisted
from django.contrib.auth.models import Permission

import warnings


class BaseObjectPermissionManager(models.Manager):
    @property
    def user_or_group_field(self):
        try:
            self.model._meta.get_field('user')
            return 'user'
        except FieldDoesNotExist:
            return 'group'
    def is_generic(self):
        try:
            self.model._meta.get_field('object_pk')
            return True
        except FieldDoesNotExist:
            return False
    def assign_perm(self, perm, user_or_group, object):
        if getattr(object, 'pk', None) is None:
            raise ObjectNotPersisted('Object %s needs to be persisted first' % object)
        ctype = get_content_type(object)
        if not isinstance(perm, Permission):
            permission = Permission.objects.get(content_type=ctype, codename=perm)
        else:
            permission = perm
        kwargs = {'permission': permission, self.user_or_group_field: user_or_group}
        if self.is_generic():
            kwargs['content_type'] = ctype
            kwargs['object_pk'] = object.pk
        else:
            kwargs['content_object'] = object
        obj_perm, _ = self.get_or_create(**kwargs)
        return obj_perm

    def bulk_assign_perm(self, perm, user_or_group, queryset):
        if isinstance(queryset, list):
            ctype = get_content_type(queryset[0])
        else:
            ctype = get_content_type(queryset.model)
        if not isinstance(perm, Permission):
            permission = Permission.objects.get(content_type=ctype, codename=perm)
        else:
            permission = perm
        checker = ObjectPermissionChecker(user_or_group)
        checker.prefetch_perms(queryset)
        assigned_perms = []
        for instance in queryset:
            if not checker.has_perm(permission.codename, instance):
                kwargs = {'permission': permission, self.user_or_group_field: user_or_group}
                if self.is_generic():
                    kwargs['content_type'] = ctype
                    kwargs['object_pk'] = instance.pk
                else:
                    kwargs['content_object'] = instance
                assigned_perms.append(self.model(**kwargs))
        self.model.objects.bulk_create(assigned_perms)
        return assigned_perms

    def assign_perm_to_many(self, perm, users_or_groups, object):
        ctype = get_content_type(object)
        if not isinstance(perm, Permission):
            permission = Permission.objects.get(content_type=ctype, codename=perm)
        else:
            permission = perm
        kwargs = {'permission': permission}
        if self.is_generic():
            kwargs['content_type'] = ctype
            kwargs['object_pk'] = object.pk
        else:
            kwargs['content_object'] = object
        to_add = []
        field = self.user_or_group_field
        for user in users_or_groups:
            kwargs[field] = user
            to_add.append(self.model(**kwargs))
        return self.model.objects.bulk_create(to_add)

    def assign(self, perm, user_or_group, object):
        warnings.warn('''UserObjectPermissionManager method 'assign' is being renamed to 'assign_perm'. Update your code accordingly as old name will be depreciated in 2.0 version.''', DeprecationWarning)
        return self.assign_perm(perm, user_or_group, object)

    def remove_perm(self, perm, user_or_group, object):
        if getattr(object, 'pk', None) is None:
            raise ObjectNotPersisted('Object %s needs to be persisted first' % object)
        filters = Q(**{self.user_or_group_field: user_or_group})
        if isinstance(perm, Permission):
            filters &= Q(permission=perm)
        else:
            filters &= Q(permission__codename=perm, permission__content_type=get_content_type(object))
        if self.is_generic():
            filters &= Q(object_pk=object.pk)
        else:
            filters &= Q(content_object__pk=object.pk)
        return self.filter(filters).delete()

    def bulk_remove_perm(self, perm, user_or_group, queryset):
        filters = Q(**{self.user_or_group_field: user_or_group})
        if isinstance(perm, Permission):
            filters &= Q(permission=perm)
        else:
            ctype = get_content_type(queryset.model)
            filters &= Q(permission__codename=perm, permission__content_type=ctype)
        if self.is_generic():
            filters &= Q(object_pk__in=[str(pk) for pk in queryset.values_list('pk', flat=True)])
        else:
            filters &= Q(content_object__in=queryset)
        return self.filter(filters).delete()


class UserObjectPermissionManager(BaseObjectPermissionManager):
    pass


class GroupObjectPermissionManager(BaseObjectPermissionManager):
    pass
