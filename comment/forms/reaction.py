import logging

from django import forms
from django.utils.translation import gettext_lazy as _

from comment.models import CommentFlag, CommentReaction

logger = logging.getLogger(__name__)


class CommentReactionCreateForm(forms.Form):
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
    reaction_type = forms.IntegerField(
        label=_('Reaction'),
        widget=forms.NumberInput(
            attrs={
                'placeholder': _('Your reaction type'),
                'id': 'reaction_type',
                'class': ''
            }),
    )

    class Meta:
        model = CommentReaction
        fields = [
            'comment_id',
            'reaction_type',
        ]
