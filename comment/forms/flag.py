import logging

from django import forms
from django.utils.translation import gettext_lazy as _

from comment.models import CommentFlag

logger = logging.getLogger(__name__)


class CommentFlagCreateForm(forms.Form):
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
    reason = forms.CharField(
        label=_('Reason'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Your reason'),
                'id': 'reason',
                'class': ''
            }),
    )

    class Meta:
        model = CommentFlag
        fields = [
            'comment_id',
            'reason',
        ]
