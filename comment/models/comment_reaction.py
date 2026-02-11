import logging
from enum import IntEnum, unique

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from comment import settings
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


class CommentReaction(TimeStamped, SoftDeletable, ):
    id = ShortUUIDField(
        length=25,
        primary_key=True,
        verbose_name=_('id'),
        help_text=_('Used for identity'),
    )
    comment = models.OneToOneField(
        to=Comment,
        related_name='reaction',
        on_delete=models.CASCADE,
        verbose_name=_('comment'),
        help_text=_('Used for linked key comment'),
    )
    like = models.PositiveIntegerField(
        default=0,
        verbose_name=_('like'),
        help_text=_('Used for count like'),
    )
    dislike = models.PositiveIntegerField(
        default=0,
        verbose_name=_('dislike'),
        help_text=_('Used for count dislike'),
    )
    tracker = Tracker()
    history = History(
        table_name=u'\"history".\"{}_comment_reaction\"'.format(settings.SCHEMA),
        verbose_name=_('Used store history comment reaction'),
        excluded_fields=['modified', ],
    )

    class Meta:
        managed = True
        db_table = u'\"{}\".\"comment_reaction\"'.format(settings.SCHEMA)
        verbose_name = _('Used store comment reaction')

    def increase_count(self, field):
        self.refresh_from_db()
        setattr(self, field, getattr(self, field, 0) + 1)
        self.save(update_fields=[field])

    def decrease_count(self, field):
        self.refresh_from_db()
        setattr(self, field, getattr(self, field, 0) - 1)
        self.save(update_fields=[field])

    def increase_reaction_count(self, reaction: int):
        if reaction == CommentReactionReason.Type.LIKE.value:
            self.increase_count('like')
        else:
            self.increase_count('dislike')

    def decrease_reaction_count(self, reaction: int):
        if reaction == CommentReactionReason.Type.LIKE.value:
            self.decrease_count('like')
        else:
            self.decrease_count('dislike')


class CommentReactionReason(TimeStamped, SoftDeletable, ):
    @unique
    class Type(IntEnum, ):
        LIKE = 1
        DISLIKE = 2

    ReactionType = [
        (type.value, type.name,) for type in Type
    ]
    id = ShortUUIDField(
        length=25,
        primary_key=True,
        verbose_name=_('id'),
        help_text=_('Used for identity'),
    )
    reaction = models.ForeignKey(
        to=CommentReaction,
        related_name='reactions',
        on_delete=models.CASCADE,
        verbose_name=_('reaction'),
        help_text=_('Used for linked key reaction'),
    )
    user = models.ForeignKey(
        to=User,
        related_name='reactions',
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        help_text=_('Used for linked key user'),
    )
    reaction_type = models.SmallIntegerField(
        choices=ReactionType,
        verbose_name=_('reaction type'),
        help_text=_('Used for reaction type like or dislike'),
    )
    tracker = Tracker()
    history = History(
        table_name=u'\"history".\"{}_reaction_reason\"'.format(settings.SCHEMA),
        verbose_name=_('Used store history comment reaction reason'),
        excluded_fields=['modified', ],
    )

    class Meta:
        managed = True
        db_table = u'\"{}\".\"comment_reaction_reason\"'.format(settings.SCHEMA)
        verbose_name = _('Used store comment reaction reason')
        unique_together = (('user', 'reaction',),)
