from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.fields import ShortUUIDField
from permission import settings
from permission.compat import user_model_label
from permission.content_types import get_content_type
from permission.managers import GroupObjectPermissionManager, UserObjectPermissionManager


class BaseObjectPermission(models.Model):
    permission = models.ForeignKey(to=Permission, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return '{}, {}, {}'.format(str(self.content_object), str(getattr(self, 'user', False) or self.group), str(self.permission.codename))

    def save(self, *args, **kwargs):
        content_type = get_content_type(self.content_object)
        if content_type != self.permission.content_type:
            raise ValidationError('''Cannot persist permission not designed for this class (permission's type is %r and object's type is %r)''' % (self.permission.content_type, content_type))
        return super().save(*args, **kwargs)


class BaseGenericObjectPermission(models.Model):
    content_type = models.ForeignKey(
        to=ContentType,
        on_delete=models.CASCADE,
        verbose_name=_('content type'),
        help_text=_('Used for linked key content type'),
    )
    object_pk = models.CharField(
        verbose_name=_('object id'),
        help_text=_('Used for linked key object'),
    )
    content_object = GenericForeignKey(
        fk_field='object_pk',
    )

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['content_type', 'object_pk']),
        ]


class UserObjectPermissionBase(BaseObjectPermission):
    user = models.ForeignKey(
        to=user_model_label,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        help_text=_('Used for linked key user'),
    )
    objects = UserObjectPermissionManager()

    class Meta:
        abstract = True
        unique_together = ['user', 'permission', 'content_object']


class UserObjectPermissionAbstract(UserObjectPermissionBase, BaseGenericObjectPermission):
    class Meta(UserObjectPermissionBase.Meta, BaseGenericObjectPermission.Meta):
        abstract = True
        unique_together = ['user', 'permission', 'object_pk']


class UserObjectPermission(UserObjectPermissionAbstract):
    id = ShortUUIDField(
        length=25,
        primary_key=True,
        verbose_name=_('object permission user id'),
        help_text=_('Used for identity'),
    )

    class Meta(UserObjectPermissionAbstract.Meta):
        abstract = False
        db_table = u'\"{}\".\"object_permission_user\"'.format(settings.SCHEMA)
        verbose_name = _('Used store user object permission')


class GroupObjectPermissionBase(BaseObjectPermission):
    group = models.ForeignKey(
        to=Group,
        on_delete=models.CASCADE,
        verbose_name=_('group'),
        help_text=_('Used for linked key group'),
    )
    objects = GroupObjectPermissionManager()

    class Meta:
        abstract = True
        unique_together = ['group', 'permission', 'content_object']


class GroupObjectPermissionAbstract(GroupObjectPermissionBase, BaseGenericObjectPermission):
    class Meta(GroupObjectPermissionBase.Meta, BaseGenericObjectPermission.Meta):
        abstract = True
        unique_together = ['group', 'permission', 'object_pk']


class GroupObjectPermission(GroupObjectPermissionAbstract):
    id = ShortUUIDField(
        length=25,
        primary_key=True,
        verbose_name=_('object permission group id'),
        help_text=_('Used for identity'),
    )

    class Meta(GroupObjectPermissionAbstract.Meta):
        abstract = False
        db_table = u'\"{}\".\"object_permission_group\"'.format(settings.SCHEMA)
        verbose_name = _('Used store group object permission')
