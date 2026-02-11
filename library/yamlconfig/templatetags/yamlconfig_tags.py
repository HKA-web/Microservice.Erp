"""
Custom template filters to support display of YAMLCONF values via HTML views.
"""
from django import template

register = template.Library()


@register.filter
def get_type(value):
    """
    Return the name of the type for a value.  This is used when displaying
    values via HTML templates.
    """
    return type(value).__name__
