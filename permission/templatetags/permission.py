from django import template
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group

from permission.core import ObjectPermissionChecker
from permission.exceptions import NotUserNorGroup

register = template.Library()


class ObjectPermissionsNode(template.Node):
    def __init__(self, for_whom, object, context_var, checker=None):
        self.for_whom = template.Variable(for_whom)
        self.object = template.Variable(object)
        self.context_var = context_var
        self.checker = template.Variable(checker) if checker else None

    def render(self, context):
        for_whom = self.for_whom.resolve(context)
        if isinstance(for_whom, get_user_model()):
            self.user = for_whom
            self.group = None
        elif isinstance(for_whom, AnonymousUser):
            self.user = get_user_model().get_anonymous()
            self.group = None
        elif isinstance(for_whom, Group):
            self.user = None
            self.group = for_whom
        else:
            raise NotUserNorGroup('User or Group instance required (got %s)' % for_whom.__class__)
        object = self.object.resolve(context)
        if not object:
            return ''
        check = self.checker.resolve(context) if self.checker else ObjectPermissionChecker(for_whom)
        perms = check.get_perms(object)
        context[self.context_var] = perms
        return ''


@register.tag
def get_object_perms(parser, token):
    bits = token.split_contents()
    format = '{% get_object_perms user/group for object as `context_var` perm_checker %}'
    if not (6 <= len(bits) <= 7) or bits[2] != 'for' or bits[4] != 'as':
        raise template.TemplateSyntaxError('get_obj_perms tag should be in format: %s' % format)
    for_whom = bits[1]
    object = bits[3]
    context_var = bits[5]
    if context_var[0] != context_var[-1] or context_var[0] not in ('"', "'"):
        raise template.TemplateSyntaxError('''get_object_perms tag's context_var argument should be in quotes''')
    context_var = context_var[1:-1]
    checker = bits[6] if len(bits) == 7 else None
    return ObjectPermissionsNode(for_whom, object, context_var, checker)
