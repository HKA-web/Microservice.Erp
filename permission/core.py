from itertools import chain

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db.models.query import QuerySet
from django.utils.encoding import force_str

from permission import settings
from permission.content_types import get_content_type
from permission.utils import get_group_object_perms_model, get_identity, get_user_object_perms_model


def _get_pks_model_and_ctype(objects):
    if isinstance(objects, QuerySet):
        model = objects.model
        pks = [force_str(pk) for pk in objects.values_list('pk', flat=True)]
        ctype = get_content_type(model)
    else:
        pks = []
        for idx, object in enumerate(objects):
            if not idx:
                model = type(object)
                ctype = get_content_type(model)
            pks.append(force_str(object.pk))
    return pks, model, ctype


class ObjectPermissionChecker:
    def __init__(self, user_or_group=None):
        self.user, self.group = get_identity(user_or_group)
        self._object_perms_cache = {}
    def has_perm(self, perm, object):
        if self.user and not self.user.is_active:
            return False
        elif self.user and self.user.is_superuser:
            return True
        if '.' in perm:
            _, perm = perm.split('.', 1)
        return perm in self.get_perms(object)

    def get_group_filters(self, object):
        User = get_user_model()
        ctype = get_content_type(object)
        group_model = get_group_object_perms_model(object)
        group_rel_name = group_model.permission.field.related_query_name()
        if self.user:
            fieldname = '{}__group__{}'.format(
                group_rel_name,
                User.groups.field.related_query_name(),
            )
            group_filters = {fieldname: self.user}
        else:
            group_filters = {'%s__group' % group_rel_name: self.group}
        if group_model.objects.is_generic():
            group_filters.update({
                '%s__content_type' % group_rel_name: ctype,
                '%s__object_pk' % group_rel_name: object.pk,
            })
        else:
            group_filters['%s__content_object' % group_rel_name] = object
        return group_filters

    def get_user_filters(self, object):
        ctype = get_content_type(object)
        model = get_user_object_perms_model(object)
        related_name = model.permission.field.related_query_name()
        user_filters = {'%s__user' % related_name: self.user}
        if model.objects.is_generic():
            user_filters.update({
                '%s__content_type' % related_name: ctype,
                '%s__object_pk' % related_name: object.pk,
            })
        else:
            user_filters['%s__content_object' % related_name] = object

        return user_filters

    def get_user_perms(self, object):
        ctype = get_content_type(object)
        perms_qs = Permission.objects.filter(content_type=ctype)
        user_filters = self.get_user_filters(object)
        user_perms_qs = perms_qs.filter(**user_filters)
        user_perms = user_perms_qs.values_list('codename', flat=True)
        return user_perms

    def get_group_perms(self, object):
        ctype = get_content_type(object)
        perms_qs = Permission.objects.filter(content_type=ctype)
        group_filters = self.get_group_filters(object)
        group_perms_qs = perms_qs.filter(**group_filters)
        group_perms = group_perms_qs.values_list('codename', flat=True)
        return group_perms

    def get_perms(self, object):
        if self.user and not self.user.is_active:
            return []
        if settings.AUTO_PREFETCH:
            self._prefetch_cache()
        ctype = get_content_type(object)
        key = self.get_local_cache_key(object)
        if key not in self._object_perms_cache:
            if settings.AUTO_PREFETCH:
                return []
            if self.user and self.user.is_superuser:
                perms = list(Permission.objects.filter(content_type=ctype).values_list('codename', flat=True))
            elif self.user:
                user_perms = self.get_user_perms(object)
                group_perms = self.get_group_perms(object)
                perms = list(set(chain(user_perms, group_perms)))
            else:
                perms = list(set(self.get_group_perms(object)))
            self._object_perms_cache[key] = perms
        return self._object_perms_cache[key]

    def get_local_cache_key(self, object):
        ctype = get_content_type(object)
        return (ctype.id, force_str(object.pk))

    def prefetch_perms(self, objects):
        if self.user and not self.user.is_active:
            return []

        User = get_user_model()
        pks, model, ctype = _get_pks_model_and_ctype(objects)
        if self.user and self.user.is_superuser:
            perms = list(Permission.objects.filter(content_type=ctype).values_list('codename', flat=True))
            for pk in pks:
                key = (ctype.id, force_str(pk))
                self._object_perms_cache[key] = perms
            return True
        group_model = get_group_object_perms_model(model)
        if self.user:
            fieldname = 'group__{}'.format(User.groups.field.related_query_name(),)
            group_filters = {fieldname: self.user}
        else:
            group_filters = {'group': self.group}
        if group_model.objects.is_generic():
            group_filters.update({
                'content_type': ctype,
                'object_pk__in': pks,
            })
        else:
            group_filters.update({
                'content_object_id__in': pks
            })
        if self.user:
            model = get_user_object_perms_model(model)
            user_filters = {
                'user': self.user,
            }
            if model.objects.is_generic():
                user_filters.update({
                    'content_type': ctype,
                    'object_pk__in': pks
                })
            else:
                user_filters.update({
                    'content_object_id__in': pks
                })
            user_perms_qs = model.objects.filter(**user_filters).select_related('permission')
            group_perms_qs = group_model.objects.filter(**group_filters).select_related('permission')
            perms = chain(user_perms_qs, group_perms_qs)
        else:
            perms = group_model.objects.filter(**group_filters).select_related('permission')
        for object in objects:
            key = self.get_local_cache_key(object)
            if key not in self._object_perms_cache:
                self._object_perms_cache[key] = []
        for perm in perms:
            if type(perm).objects.is_generic():
                key = (ctype.id, perm.object_pk)
            else:
                key = (ctype.id, force_str(perm.content_object_id))
            self._object_perms_cache[key].append(perm.permission.codename)
        return True

    @staticmethod
    def _init_obj_prefetch_cache(object, *querysets):
        cache = {}
        for queryset in querysets:
            perms = queryset.select_related('permission__codename').values_list('content_type_id', 'object_pk', 'permission__codename')
            for perm in perms:
                if perm[:2] not in cache:
                    cache[perm[:2]] = []
                cache[perm[:2]] += [perm[2], ]
        object._permission_perms_cache = cache
        return object, cache

    def _prefetch_cache(self):
        from permission.utils import get_user_object_perms_model, get_group_object_perms_model
        UserObjectPermission = get_user_object_perms_model()
        GroupObjectPermission = get_group_object_perms_model()
        if self.user:
            object = self.user
            querysets = [
                UserObjectPermission.objects.filter(user=object),
                GroupObjectPermission.objects.filter(group__user=object)
            ]
        else:
            object = self.group
            querysets = [
                GroupObjectPermission.objects.filter(group=object),
            ]

        if not hasattr(object, '_permission_perms_cache'):
            object, cache = self._init_obj_prefetch_cache(object, *querysets)
        else:
            cache = object._permission_perms_cache
        self._object_perms_cache = cache
