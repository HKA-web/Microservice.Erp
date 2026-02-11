import logging

from django import template

from comment.models import CommentReactionReason, CommentFlagReason

logger = logging.getLogger(__name__)

register = template.Library()


@register.filter(name='commentliked')
@register.simple_tag(name='commentliked', takes_context=True)
def liked(context, comment):
    user = context['request'].user
    return CommentReactionReason.objects.filter(
        reaction__comment__pk=comment.pk,
        reaction_type=CommentReactionReason.Type.LIKE,
        user_id=user.pk
    ).exists()


@register.filter(name='commentdisliked')
@register.simple_tag(name='commentdisliked', takes_context=True)
def disliked(context, comment):
    user = context['request'].user
    return CommentReactionReason.objects.filter(
        reaction__comment__pk=comment.pk,
        reaction_type=CommentReactionReason.Type.DISLIKE,
        user_id=user.pk
    ).exists()


@register.filter(name='commentflaged')
@register.simple_tag(name='commentflaged', takes_context=True)
def flaged(context, comment):
    user = context['request'].user
    return CommentFlagReason.objects.filter(
        flag__comment__pk=comment.pk,
        user_id=user.pk
    ).exists()
