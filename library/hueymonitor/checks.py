from django.conf import settings
from django.core.checks import Warning, register


@register()
def hueymonitor_check(app_configs, **kwargs):
    errors = []

    if 'library.hueymonitorutils' not in settings.INSTALLED_APPS:
        # hueymonitorutils is needed for "humanize_time" template library
        # See: https://github.com/boxine/django-huey-monitor/issues/21
        errors.append(
            Warning(
                '"library.hueymonitorutils" not in INSTALLED_APPS',
                id='hueymonitor.E001',
            )
        )

    return errors
