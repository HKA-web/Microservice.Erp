import logging
from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View

from comment.forms import CommentCreateForm
from comment.models import Comment
from library.renderblock.base import render_block_to_string

logger = logging.getLogger(__name__)


class CommentView(LoginRequiredMixin, PermissionRequiredMixin, View, ):
    permission_required = [
        'comment.view_comment',
    ]

    def get(self, request, pk=None, object=None, offset=None, ):
        try:
            content_type = ContentType.objects.get(pk=pk)
        except ContentType.DoesNotExist:
            content_type = ContentType.objects.filter(pk=request.GET.get('object_content_id')).first()
        Model = content_type.model_class()
        try:
            object = Model.objects.get(pk=object)
        except ContentType.DoesNotExist:
            object = Model.objects.filter(pk=request.GET.get('object_id')).first()
        if offset is not None:
            return JsonResponse(dict(
                html=render_block_to_string(
                    'comment/index.html',
                    'partial',
                    context=dict(
                        comment=Comment.objects.select_related('user', 'reaction', 'flag').filter(
                            content_type=content_type,
                            object_id=object.pk,
                            parent_id=None
                        ).order_by('-created')[int(offset):int(offset) + 10],
                        form=CommentCreateForm,
                    ),
                    request=request,
                ),
            ), safe=False, status=HTTPStatus.OK, )
        return render(request, 'comment/index.html', dict(
            comment=Comment.objects.select_related('user', 'reaction', 'flag').filter(
                content_type=content_type,
                object_id=object.pk,
                parent_id=None
            ).order_by('-created')[0:10],
            form=CommentCreateForm,
            content_type=content_type,
            object=object,
        ))

    def post(self, request, ):
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            post = request.POST.dict()
            data = dict(
                user=request.user,
                **post,
            )
            if ('parent_id' in post and post['parent_id'] is not None):
                comment = Comment.objects.create(**data)
            else:
                comment = Comment.objects.create(**data)
            return JsonResponse(dict(
                message=_('Comment %(comment_id)s have been successfully created') % dict(comment_id=comment.comment_id),
                comment=post,
                html=render_block_to_string(
                    'comment/index.html',
                    'partial',
                    context=dict(
                        comment=Comment.objects.select_related('user', 'reaction', 'flag').filter(pk=comment.pk),
                        form=CommentCreateForm,
                    ),
                    request=request,
                ),
            ), safe=False, status=HTTPStatus.OK, )
        else:
            return JsonResponse(dict(
                error=_(u'Data validation error'),
                validation=form.errors
            ), safe=False, status=HTTPStatus.BAD_REQUEST, )

    def delete(self, request, pk=None, ):
        if request.method in ('DELETE'):
            post = request.DELETE.dict()
            try:
                comment = Comment.objects.get(pk=pk)
            except Comment.DoesNotExist:
                comment = Comment.objects.get(pk=post['comment_id'])
            comment.is_removed = True
            comment.save(update_fields=['is_removed'])
            return JsonResponse(dict(
                message=_('Comment %(comment_id)s have been successfully deleted') % dict(comment_id=comment.comment_id),
                comment=post,
                html=render_block_to_string(
                    'comment/index.html',
                    'partial',
                    context=dict(
                        comment=Comment.objects.select_related('user', 'reaction', 'flag').filter(pk=comment.pk),
                        form=CommentCreateForm,
                    ),
                    request=request,
                ),
            ), safe=False, status=HTTPStatus.OK, )
        else:
            return JsonResponse(dict(
                error=_(u'Data validation error'),
            ), safe=False, status=HTTPStatus.BAD_REQUEST, )
