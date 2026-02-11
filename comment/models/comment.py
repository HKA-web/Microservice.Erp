import logging

from django.conf import settings as djangosettings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Model
from django.utils.translation import gettext_lazy as _

from comment import settings
from core.fields import ShortUUIDField, StatusField
from core.models import AdjacencyListTree, TimeStamped, SoftDeletable, BaseStatus, History, Tracker
from library import timeago

logger = logging.getLogger(__name__)

try:
    from django.contrib.auth import get_user_model

    User = get_user_model()
except:
    User = djangosettings.AUTH_USER_MODEL


class Comment(BaseStatus, AdjacencyListTree, TimeStamped, SoftDeletable, ):
    node_order_by = ['object_id', ]
    comment_id = ShortUUIDField(
        length=25,
        primary_key=True,
        verbose_name=_('comment id'),
        help_text=_('Used for identity'),
    )
    parent = models.ForeignKey(
        to='self',
        on_delete=models.DO_NOTHING,
        related_name='children_set',
        blank=True,
        null=True,
        verbose_name=_('parent'),
        help_text=_('Used for hierarchy parent id'),
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_('user'),
        help_text=_('Used for linked key author comment'),
    )
    content_type = models.ForeignKey(
        to=ContentType,
        on_delete=models.CASCADE,
        verbose_name=_('content type'),
        help_text=_('Used for linked key model comment'),
    )
    object_id = models.CharField(
        blank=False,
        null=False,
        verbose_name=_('object id'),
        help_text=_('Used for linked key commented object'),
    )
    content_object = GenericForeignKey('content_type', 'object_id', )
    message = models.TextField(
        verbose_name=_('message'),
    )
    read_only = models.BooleanField(
        default=False,
        verbose_name=_('read only'),
        help_text=_('Used for disable modification'),
    )
    status = StatusField(transition=False, )
    tracker = Tracker()
    history = History(
        bases=[BaseStatus, Model, ],
        table_name=u'\"history".\"{}_comment\"'.format(settings.SCHEMA),
        verbose_name=_('Used store history comment'),
        excluded_fields=['modified', ],
    )

    class Meta:
        managed = True
        db_table = u'\"{}\".\"comment\"'.format(settings.SCHEMA)
        verbose_name = _('Used store comment')

    def get_children(self):
        return super(Comment, self).get_children().filter(
            parent=self,
            is_removed=False,
        )

    @property
    def flages(self):
        return getattr(self.flag, 'count', 0)

    @property
    def likes(self):
        return getattr(self.reaction, 'like', 0)

    @property
    def dislikes(self):
        return getattr(self.reaction, 'dislike', 0)

    @property
    def age(self):
        return timeago.format(self.created, locale='id')


    @property
    def message_translated(self):
        return ' '.join(' '.join([
            _(str(_(message)).title())
            .replace('Jan', str(_('Jan')))
            .replace('Feb', str(_('Feb')))
            .replace('Mar', str(_('Mar')))
            .replace('Apr', str(_('Apr')))
            .replace('May', str(_('May')))
            .replace('Jun', str(_('Jun')))
            .replace('Jul', str(_('Jul')))
            .replace('Aug', str(_('Aug')))
            .replace('Sep', str(_('Sep')))
            .replace('Oct', str(_('Oct')))
            .replace('Nov', str(_('Nov')))
            .replace('Dec', str(_('Dec')))
            .replace('Sunday', str(_('Sunday')))
            .replace('Monday', str(_('Monday')))
            .replace('Tuesday', str(_('Tuesday')))
            .replace('Wednesday', str(_('Wednesday')))
            .replace('Thursday', str(_('Thursday')))
            .replace('Friday', str(_('Friday')))
            .replace('Saturday', str(_('Saturday')))
            .replace('Changed', str(_('Changed')))
            .replace('To', str(_('To')))
            .replace('True', str(_('True')))
            .replace('False', str(_('False'))) for message in (self.message.title()).split()
        ]).split())
