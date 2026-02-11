import logging

from django import forms
from django.utils.translation import gettext_lazy as _

from comment.models import Comment

logger = logging.getLogger(__name__)


class CommentCreateForm(forms.Form):
    comment_id = forms.CharField(
        label=_('Comment ID'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Your comment id'),
                'id': 'comment_id',
                'class': ''
            }),
        required=False,
    )
    parent_id = forms.CharField(
        label=_('Parent Comment'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Your parent comment'),
                'id': 'parent_id',
                'class': ''
            }),
        required=False,
    )
    content_type_id = forms.IntegerField(
        label=_('Content Type'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Your content type'),
                'id': 'content_type_id',
                'class': ''
            }),
    )
    object_id = forms.CharField(
        label=_('Object ID'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Your object id'),
                'id': 'object_id',
                'class': ''
            }),
    )
    message = forms.CharField(
        label=_('Message'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Your message'),
                'id': 'message',
                'class': ''
            }),
    )

    class Meta:
        model = Comment
        fields = [
            'comment_id',
            'parent_id',
            'content_type_id',
            'object_id',
            'message',
        ]
