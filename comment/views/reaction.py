import logging
from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core import exceptions
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import View

from comment.forms import CommentFlagCreateForm, CommentReactionCreateForm
from comment.models import Comment, CommentReaction, CommentReactionReason
from core.mixins import AtomicMixin
from library.renderblock.base import render_block_to_string

logger = logging.getLogger(__name__)


class CommentReactionView(LoginRequiredMixin, PermissionRequiredMixin, AtomicMixin, View):
    permission_required = [
        'comment.view_commentreaction',
        'comment.add_commentreaction',
    ]

    def get(self, request, ):
        pass

    def post(self, request):
        form = CommentReactionCreateForm(request.POST)
        if form.is_valid():
            post = request.POST.dict()
            comment = Comment.objects.select_related('reaction').get(pk=post['comment_id'])
            try:
                reaction = comment.reaction
            except exceptions.ObjectDoesNotExist:
                reaction = CommentReaction.objects.create(
                    comment=comment,
                )
            reason, created = CommentReactionReason.objects.get_or_create(
                reaction=reaction,
                user=request.user,
                defaults=dict(reaction_type=int(post['reaction_type'])),
            )
            if created:
                reaction.increase_reaction_count(reason.reaction_type)
            else:
                reaction.decrease_reaction_count(reason.reaction_type)
                reason.reaction_type = int(post['reaction_type'])
                reason.save()
                reaction.increase_reaction_count(int(post['reaction_type']))
            return JsonResponse(dict(
                message=_('Comment reaction %(reaction_id)s, reason %(reason_id)s have been successfully %(created)s') % dict(reaction_id=reaction.id, reason_id=reason.id, created=_('created') if created else _('updated')),
                comment=post,
                html=render_block_to_string(
                    'comment/index.html',
                    'partial',
                    context=dict(
                        comment=Comment.objects.filter(pk=comment.pk),
                        form=CommentFlagCreateForm,
                    ),
                    request=request,
                ),
            ), safe=False, status=HTTPStatus.OK, )
        else:
            return JsonResponse(dict(
                error=_(u'Data validation error'),
                validation=form.errors
            ), safe=False, status=HTTPStatus.BAD_REQUEST, )
