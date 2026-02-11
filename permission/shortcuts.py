import warnings
from collections import defaultdict
from functools import partial
from itertools import groupby

from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.db.models import (
    AutoField,
    BigIntegerField,
    CharField,
    ForeignKey,
    IntegerField,
    PositiveIntegerField,
    PositiveSmallIntegerField,
    SmallIntegerField,
    UUIDField,
)
from django.db.models import Count, Q, QuerySet
from django.db.models.expressions import Value
from django.db.models.functions import Cast, Replace
from django.shortcuts import _get_queryset

from permission.core import ObjectPermissionChecker
from permission.content_types import get_content_type
from permission.exceptions import MixedContentTypeError, WrongAppError, MultipleIdentityAndObjectError
from permission.utils import get_anonymous_user, get_group_object_perms_model, get_identity, get_user_object_perms_model

GroupObjectPermission = get_group_object_perms_model()
UserObjectPermission = get_user_object_perms_model()


def assign_perm(perm, user_or_group, obj=None):
    user, group = get_identity(user_or_group)
    if obj is None:
        if not isinstance(perm, Permission):
            try:
                app_label, codename = perm.split('.', 1)
            except ValueError:
                raise ValueError('''For global permissions, first argument must be in format: 'app_label.codename' (is %r)''' % perm)
            perm = Permission.objects.get(content_type__app_label=app_label, codename=codename)
        if user:
            user.user_permissions.add(perm)
            return perm
        if group:
            group.permissions.add(perm)
            return perm
    if not isinstance(perm, Permission):
        if '.' in perm:
            app_label, perm = perm.split('.', 1)

    if isinstance(obj, (QuerySet, list)):
        if isinstance(user_or_group, (QuerySet, list)):
            raise MultipleIdentityAndObjectError('Only bulk operations on either users/groups OR objects supported')
        if user:
            model = get_user_object_perms_model(obj[0] if isinstance(obj, list) else obj.model)
            return model.objects.bulk_assign_perm(perm, user, obj)
        if group:
            model = get_group_object_perms_model(obj[0] if isinstance(obj, list) else obj.model)
            return model.objects.bulk_assign_perm(perm, group, obj)

    if isinstance(user_or_group, (QuerySet, list)):
        if user:
            model = get_user_object_perms_model(obj)
            return model.objects.assign_perm_to_many(perm, user, obj)
        if group:
            model = get_group_object_perms_model(obj)
            return model.objects.assign_perm_to_many(perm, group, obj)
    if user:
        model = get_user_object_perms_model(obj)
        return model.objects.assign_perm(perm, user, obj)
    if group:
        model = get_group_object_perms_model(obj)
        return model.objects.assign_perm(perm, group, obj)


def assign(perm, user_or_group, obj=None):
    warnings.warn('''Shortcut function 'assign' is being renamed to 'assign_perm'. Update your code accordingly as old name will be depreciated in 2.0 version.''', DeprecationWarning)
    return assign_perm(perm, user_or_group, obj)


def remove_perm(perm, user_or_group=None, obj=None):
    user, group = get_identity(user_or_group)
    if obj is None:
        if not isinstance(perm, Permission):
            try:
                app_label, codename = perm.split('.', 1)
            except ValueError:
                raise ValueError('''For global permissions, first argument must be in format: 'app_label.codename' (is %r)''' % perm)
            perm = Permission.objects.get(content_type__app_label=app_label, codename=codename)
        if user:
            user.user_permissions.remove(perm)
            return
        if group:
            group.permissions.remove(perm)
            return
    if not isinstance(perm, Permission):
        perm = perm.split('.')[-1]
    if isinstance(obj, QuerySet):
        if user:
            model = get_user_object_perms_model(obj.model)
            return model.objects.bulk_remove_perm(perm, user, obj)
        if group:
            model = get_group_object_perms_model(obj.model)
            return model.objects.bulk_remove_perm(perm, group, obj)
    if user:
        model = get_user_object_perms_model(obj)
        return model.objects.remove_perm(perm, user, obj)
    if group:
        model = get_group_object_perms_model(obj)
        return model.objects.remove_perm(perm, group, obj)


def get_perms(user_or_group, obj):
    check = ObjectPermissionChecker(user_or_group)
    return check.get_perms(obj)


def get_user_perms(user, obj):
    check = ObjectPermissionChecker(user)
    return check.get_user_perms(obj)


def get_group_perms(user_or_group, obj):
    check = ObjectPermissionChecker(user_or_group)
    return check.get_group_perms(obj)


def get_perms_for_model(cls):
    if isinstance(cls, str):
        app_label, model_name = cls.split('.')
        model = apps.get_model(app_label, model_name)
    else:
        model = cls
    ctype = get_content_type(model)
    return Permission.objects.filter(content_type=ctype)


def get_users_with_perms(obj, attach_perms=False, with_superusers=False, with_group_users=True, only_with_perms_in=None):
    ctype = get_content_type(obj)
    if not attach_perms:
        user_model = get_user_object_perms_model(obj)
        related_name = user_model.user.field.related_query_name()
        if user_model.objects.is_generic():
            user_filters = {
                '%s__content_type' % related_name: ctype,
                '%s__object_pk' % related_name: obj.pk,
            }
        else:
            user_filters = {'%s__content_object' % related_name: obj}
        qset = Q(**user_filters)
        if only_with_perms_in is not None:
            permission_ids = Permission.objects.filter(content_type=ctype, codename__in=only_with_perms_in).values_list('id', flat=True)
            qset &= Q(**{
                '%s__permission_id__in' % related_name: permission_ids,
            })
        if with_group_users:
            group_model = get_group_object_perms_model(obj)
            if group_model.objects.is_generic():
                group_obj_perm_filters = {
                    'content_type': ctype,
                    'object_pk': obj.pk,
                }
            else:
                group_obj_perm_filters = {
                    'content_object': obj,
                }
            if only_with_perms_in is not None:
                group_obj_perm_filters.update({
                    'permission_id__in': permission_ids,
                })
            group_ids = set(group_model.objects.filter(**group_obj_perm_filters).values_list('group_id', flat=True).distinct())
            qset = qset | Q(groups__in=group_ids)
        if with_superusers:
            qset = qset | Q(is_superuser=True)
        return get_user_model().objects.filter(qset).distinct()
    else:
        users = {}
        for user in get_users_with_perms(
            obj,
            with_group_users=with_group_users,
            only_with_perms_in=only_with_perms_in,
            with_superusers=with_superusers
        ):
            if with_group_users or with_superusers:
                users[user] = sorted(get_perms(user, obj))
            else:
                users[user] = sorted(get_user_perms(user, obj))
        return users


def get_groups_with_perms(obj, attach_perms=False):
    ctype = get_content_type(obj)
    group_model = get_group_object_perms_model(obj)
    if not attach_perms:
        group_rel_name = group_model.group.field.related_query_name()
        if group_model.objects.is_generic():
            group_filters = {
                '%s__content_type' % group_rel_name: ctype,
                '%s__object_pk' % group_rel_name: obj.pk,
            }
        else:
            group_filters = {'%s__content_object' % group_rel_name: obj}
        return Group.objects.filter(**group_filters).distinct()
    else:
        group_perms_mapping = defaultdict(list)
        groups_with_perms = get_groups_with_perms(obj)
        qs = group_model.objects.filter(group__in=groups_with_perms).prefetch_related('group', 'permission')
        if group_model is GroupObjectPermission:
            qs = qs.filter(object_pk=obj.pk, content_type=ctype)
        else:
            qs = qs.filter(content_object_id=obj.pk)

        for group_perm in qs:
            group_perms_mapping[group_perm.group].append(group_perm.permission.codename)
        return dict(group_perms_mapping)


def get_objects_for_user(user, perms, klass=None, use_groups=True, any_perm=False, with_superuser=True, accept_global_perms=True):
    if isinstance(perms, str):
        perms = [perms]
    ctype = None
    app_label = None
    codenames = set()
    for perm in perms:
        if '.' in perm:
            new_app_label, codename = perm.split('.', 1)
            if app_label is not None and app_label != new_app_label:
                raise MixedContentTypeError('Given perms must have same app label (%s != %s)' % (app_label, new_app_label))
            else:
                app_label = new_app_label
        else:
            codename = perm
        codenames.add(codename)
        if app_label is not None:
            new_ctype = ContentType.objects.get(app_label=app_label, permission__codename=codename)
            if ctype is not None and ctype != new_ctype:
                raise MixedContentTypeError('ContentType was once computed to be %s and another one %s' % (ctype, new_ctype))
            else:
                ctype = new_ctype
    if ctype is None and klass is not None:
        queryset = _get_queryset(klass)
        ctype = get_content_type(queryset.model)
    elif ctype is not None and klass is None:
        queryset = _get_queryset(ctype.model_class())
    elif klass is None:
        raise WrongAppError('Cannot determine content type')
    else:
        queryset = _get_queryset(klass)
        if ctype.model_class() != queryset.model:
            raise MixedContentTypeError('Content type for given perms and klass differs')
    if with_superuser and user.is_superuser:
        return queryset
    if user.is_anonymous:
        user = get_anonymous_user()
    global_perms = set()
    has_global_perms = False
    if accept_global_perms and with_superuser:
        for code in codenames:
            if user.has_perm(ctype.app_label + '.' + code):
                global_perms.add(code)
        for code in global_perms:
            codenames.remove(code)
        if len(global_perms) > 0 and (len(codenames) == 0 or any_perm):
            return queryset
        elif len(global_perms) > 0 and (len(codenames) > 0):
            has_global_perms = True
    user_model = get_user_object_perms_model(queryset.model)
    user_obj_perms_queryset = filter_perms_queryset_by_objects(
        user_model.objects
        .filter(user=user)
        .filter(permission__content_type=ctype),
        klass)
    if len(codenames):
        user_obj_perms_queryset = user_obj_perms_queryset.filter(permission__codename__in=codenames)
    direct_fields = ['content_object__pk', 'permission__codename']
    generic_fields = ['object_pk', 'permission__codename']
    if user_model.objects.is_generic():
        user_fields = generic_fields
    else:
        user_fields = direct_fields
    if use_groups:
        group_model = get_group_object_perms_model(queryset.model)
        group_filters = {
            'permission__content_type': ctype,
            'group__%s' % get_user_model().groups.field.related_query_name(): user,
        }
        if len(codenames):
            group_filters.update({
                'permission__codename__in': codenames,
            })
        groups_obj_perms_queryset = filter_perms_queryset_by_objects(
            group_model.objects.filter(**group_filters),
            klass)
        if group_model.objects.is_generic():
            group_fields = generic_fields
        else:
            group_fields = direct_fields
        if not any_perm and len(codenames) > 1 and not has_global_perms:
            user_obj_perms = user_obj_perms_queryset.values_list(*user_fields)
            groups_obj_perms = groups_obj_perms_queryset.values_list(*group_fields)
            data = list(user_obj_perms) + list(groups_obj_perms)
            keyfunc = lambda t: t[0]
            data = sorted(data, key=keyfunc)
            pk_list = []
            for pk, group in groupby(data, keyfunc):
                obj_codenames = {e[1] for e in group}
                if codenames.issubset(obj_codenames):
                    pk_list.append(pk)
            objects = queryset.filter(pk__in=pk_list)
            return objects
    if not any_perm and len(codenames) > 1:
        counts = user_obj_perms_queryset.values(
            user_fields[0]).annotate(object_pk_count=Count(user_fields[0]))
        user_obj_perms_queryset = counts.filter(
            object_pk_count__gte=len(codenames))
    field_pk = user_fields[0]
    values = user_obj_perms_queryset
    handle_pk_field = _handle_pk_field(queryset)
    if handle_pk_field is not None:
        values = values.annotate(obj_pk=handle_pk_field(expression=field_pk))
        field_pk = 'obj_pk'
    values = values.values_list(field_pk, flat=True)
    q = Q(pk__in=values)
    if use_groups:
        field_pk = group_fields[0]
        values = groups_obj_perms_queryset
        if handle_pk_field is not None:
            values = values.annotate(obj_pk=handle_pk_field(expression=field_pk))
            field_pk = 'obj_pk'
        values = values.values_list(field_pk, flat=True)
        q |= Q(pk__in=values)
    return queryset.filter(q)


def get_objects_for_group(group, perms, klass=None, any_perm=False, accept_global_perms=True):
    if isinstance(perms, str):
        perms = [perms]
    ctype = None
    app_label = None
    codenames = set()
    for perm in perms:
        if '.' in perm:
            new_app_label, codename = perm.split('.', 1)
            if app_label is not None and app_label != new_app_label:
                raise MixedContentTypeError('Given perms must have same app label (%s != %s)' % (app_label, new_app_label))
            else:
                app_label = new_app_label
        else:
            codename = perm
        codenames.add(codename)
        if app_label is not None:
            new_ctype = ContentType.objects.get(app_label=app_label, permission__codename=codename)
            if ctype is not None and ctype != new_ctype:
                raise MixedContentTypeError('ContentType was once computed to be %s and another one %s' % (ctype, new_ctype))
            else:
                ctype = new_ctype
    if ctype is None and klass is not None:
        queryset = _get_queryset(klass)
        ctype = get_content_type(queryset.model)
    elif ctype is not None and klass is None:
        queryset = _get_queryset(ctype.model_class())
    elif klass is None:
        raise WrongAppError('Cannot determine content type')
    else:
        queryset = _get_queryset(klass)
        if ctype.model_class() != queryset.model:
            raise MixedContentTypeError('Content type for given perms and klass differs')
    global_perms = set()
    if accept_global_perms:
        global_perm_set = group.permissions.values_list('codename', flat=True)
        for code in codenames:
            if code in global_perm_set:
                global_perms.add(code)
        for code in global_perms:
            codenames.remove(code)
        if len(global_perms) > 0 and (len(codenames) == 0 or any_perm):
            return queryset
    group_model = get_group_object_perms_model(queryset.model)
    groups_obj_perms_queryset = filter_perms_queryset_by_objects(
        group_model.objects
        .filter(group=group)
        .filter(permission__content_type=ctype),
        klass)
    if len(codenames):
        groups_obj_perms_queryset = groups_obj_perms_queryset.filter(
            permission__codename__in=codenames)
    if group_model.objects.is_generic():
        fields = ['object_pk', 'permission__codename']
    else:
        fields = ['content_object__pk', 'permission__codename']
    if not any_perm and len(codenames):
        groups_obj_perms = groups_obj_perms_queryset.values_list(*fields)
        data = list(groups_obj_perms)
        keyfunc = lambda t: t[0]
        data = sorted(data, key=keyfunc)
        pk_list = []
        for pk, group in groupby(data, keyfunc):
            obj_codenames = {e[1] for e in group}
            if any_perm or codenames.issubset(obj_codenames):
                pk_list.append(pk)
        objects = queryset.filter(pk__in=pk_list)
        return objects
    field_pk = fields[0]
    values = groups_obj_perms_queryset
    handle_pk_field = _handle_pk_field(queryset)
    if handle_pk_field is not None:
        values = values.annotate(obj_pk=handle_pk_field(expression=field_pk))
        field_pk = 'obj_pk'
    values = values.values_list(field_pk, flat=True)
    return queryset.filter(pk__in=values)


def _handle_pk_field(queryset):
    pk = queryset.model._meta.pk
    if isinstance(pk, ForeignKey):
        return _handle_pk_field(pk.target_field)
    if isinstance(
        pk,
        (
            IntegerField,
            AutoField,
            BigIntegerField,
            PositiveIntegerField,
            PositiveSmallIntegerField,
            SmallIntegerField,
        ),
    ):
        return partial(Cast, output_field=BigIntegerField())
    if isinstance(pk, UUIDField):
        if connection.features.has_native_uuid_field:
            return partial(Cast, output_field=UUIDField())
        return partial(
            Replace,
            text=Value('-'),
            replacement=Value(''),
            output_field=CharField(),
        )
    return None


def filter_perms_queryset_by_objects(perms_queryset, objects):
    if not isinstance(objects, QuerySet):
        return perms_queryset
    else:
        field = 'content_object__pk'
        if perms_queryset.model.objects.is_generic():
            field = 'object_pk'
        return perms_queryset.filter(**{'{}__in'.format(field): list(objects.values_list('pk', flat=True).distinct().order_by())})
