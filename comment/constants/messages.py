from django.utils.translation import gettext_lazy as _


class ExceptionError:
    pass


class ContentTypeError:
    pass


class FlagInfo:
    FlaggedSuccess = _('Comment flagged')
    UnflaggedSuccess = _('Comment flag removed')


class ReactionInfo:
    UpdatedSuccess = _('Your reaction has been updated successfully')


class FlagState:
    Unflagged = _('Unflagged')
    Flagged = _('Flagged')
    Rejected = _('Flag rejected by the moderator')
    Resolved = _('Comment modified by the author')
