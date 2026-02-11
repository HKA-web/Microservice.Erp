from django.utils.translation import gettext_lazy as _
from chatterbot.ext.django.abstract_models import AbstractBaseStatement, AbstractBaseTag


class Statement(AbstractBaseStatement):
    """
    A statement represents a single spoken entity, sentence or
    phrase that someone can say.
    """
    class Meta:
        db_table = u'\"chatbot\".\"statement\"'
        verbose_name = _('Statement')
        verbose_name_plural = _('Statements')


class Tag(AbstractBaseTag):
    """
    A label that categorizes a statement.
    """
    class Meta:
        db_table = u'\"chatbot\".\"tag\"'
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
