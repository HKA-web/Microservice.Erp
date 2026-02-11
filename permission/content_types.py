from django.contrib.contenttypes.models import ContentType
from django.utils.module_loading import import_string

from permission import settings


def get_content_type(object):
    get_content_type_function = import_string(settings.GET_CONTENT_TYPE)
    return get_content_type_function(object)


def get_default_content_type(object):
    return ContentType.objects.get_for_model(object)
