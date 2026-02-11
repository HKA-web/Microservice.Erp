import logging

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from comment import settings
from comment.constants import messages
from comment.models import Comment
from core.fields import ShortUUIDField
from core.models import (
    TimeStamped,
    SoftDeletable,
    Tracker,
    History,
)

logger = logging.getLogger(__name__)

User = get_user_model()


class CommentFlag(TimeStamped, SoftDeletable, ):
    Unflagged = 1
    Flagged = 2
    Rejected = 3
    Resolved = 4
    FlagState = [
        (Unflagged, messages.FlagState.Unflagged),
        (Flagged, messages.FlagState.Flagged),
        (Rejected, messages.FlagState.Rejected),
        (Resolved, messages.FlagState.Resolved),
    ]
    id = ShortUUIDField(
        length=25,
        primary_key=True,
        verbose_name=_('id'),
        help_text=_('Used for identity'),
    )
    comment = models.OneToOneField(
        to=Comment,
        on_delete=models.CASCADE,
        related_name='flag',
        verbose_name=_('comment'),
        help_text=_('Used for linked key comment'),
    )
    count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('count'),
        help_text=_('Used for count flag'),
    )
    state = models.SmallIntegerField(
        choices=FlagState,
        default=Unflagged,
        verbose_name=_('state'),
        help_text=_('Used for state flag'),
    )
    moderator = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('moderator'),
        help_text=_('Used for linked key moderator first flag'),
    )
    tracker = Tracker()
    history = History(
        table_name=u'\"history".\"{}_comment_flag\"'.format(settings.SCHEMA),
        verbose_name=_('Used store history comment flag'),
        excluded_fields=['modified', ],
    )

    class Meta:
        managed = True
        db_table = u'\"{}\".\"comment_flag\"'.format(settings.SCHEMA)
        verbose_name = _('Used store comment flag')

    def increase_count(self):
        self.refresh_from_db()
        self.count = self.count + 1
        self.save(update_fields=['count'])

    def decrease_count(self):
        self.refresh_from_db()
        self.count = self.count - 1
        self.save(update_fields=['count'])


class CommentFlagReason(TimeStamped, SoftDeletable, ):
    id = ShortUUIDField(
        length=25,
        primary_key=True,
        verbose_name=_('id'),
        help_text=_('Used for identity'),
    )
    flag = models.ForeignKey(
        to=CommentFlag,
        related_name='flags',
        on_delete=models.CASCADE,
        verbose_name=_('flag'),
        help_text=_('Used for linked key flag'),
    )
    user = models.ForeignKey(
        to=User,
        related_name='flags',
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        help_text=_('Used for linked key user flag'),
    )
    reason = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('reason'),
        help_text=_('Used for reason flag'),
    )
    tracker = Tracker()
    history = History(
        table_name=u'\"history".\"{}_flag_reason\"'.format(settings.SCHEMA),
        verbose_name=_('Used store history comment flag reason'),
        excluded_fields=['modified', ],
    )

    class Meta:
        managed = True
        db_table = u'\"{}\".\"comment_flag_reason\"'.format(settings.SCHEMA)
        verbose_name = _('Used store comment flag reason')
        unique_together = (('flag', 'user',),)
        ordering = ('created',)
