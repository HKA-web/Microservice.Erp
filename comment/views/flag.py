import logging
from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core import exceptions
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import View

from comment.forms import CommentFlagCreateForm
from comment.models import Comment, CommentFlag, CommentFlagReason
from core.mixins import AtomicMixin
from library.renderblock.base import render_block_to_string

logger = logging.getLogger(__name__)


class CommentFlagView(LoginRequiredMixin, PermissionRequiredMixin, AtomicMixin, View):
    permission_required = [
        'comment.view_commentflag',
        'comment.add_commentflag',
    ]

    def get(self, request, ):
        pass

    def post(self, request):
        form = CommentFlagCreateForm(request.POST)
        if form.is_valid():
            post = request.POST.dict()
            comment = Comment.objects.select_related('flag').get(pk=post['comment_id'])
            try:
                flag = comment.flag
            except exceptions.ObjectDoesNotExist:
                flag = CommentFlag.objects.create(
                    comment=comment,
                    state=CommentFlag.Flagged,
                    moderator=request.user,
                )
            reason, created = CommentFlagReason.objects.get_or_create(
                flag=flag,
                user=request.user,
                defaults=dict(reason=post['reason']),
            )
            if created:
                flag.increase_count()
            else:
                reason.reason = post['reason']
                reason.save()
            return JsonResponse(dict(
                message=_('Comment flag %(flag_id)s, reason %(reason_id)s have been successfully %(created)s') % dict(flag_id=flag.id, reason_id=reason.id, created=_('created') if created else _('updated')),
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
