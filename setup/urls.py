import logging
import sys
from importlib import import_module

from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import path, include, re_path, register_converter, URLResolver
from django.views.decorators.cache import cache_page
from django.views.i18n import JavaScriptCatalog, JSONCatalog
from django.views.static import serve

import library.jsreverse.views as reverse
from authentication.views import SigninView
from core import views
from core.models.base import Base64PkConverter
from core.utils import ShortUUID

logger = logging.getLogger(__name__)
register_converter(Base64PkConverter, Base64PkConverter.name)
key = ShortUUID().random(length=10)


def logo(request, dimen='hdpi'):
    import os
    try:
        logo = os.path.join(settings.STATIC_ROOT, f'{settings.PROJECT['LOGO']}.{dimen}.png')
        if not os.path.exists(logo):
            logo = os.path.join(settings.STATIC_ROOT, f'application/media/erpro.{dimen}.png')
        with open(logo, 'rb') as file:
            logo = file.read()
            file.close()
        return HttpResponse(logo, content_type='image/png')
    except IOError as e:
        return HttpResponseNotFound(str(e))


def urlpatterns():
    patterns = [
        path('', include('core.urls'), name='core'),
        path('admin/login/', SigninView.as_view(), name='login'),
        path('admin/', admin.site.urls, name='admin'),
        path('yamlconfig/', include('library.yamlconfig.urls'), name='yamlconfig'),
        path('', include('authentication.urls'), name='authentication'),
        path('', include('comment.urls'), name='comment'),
        path('report/', include('report.urls'), name='report'),
        path('chat/', include('chat.urls'), name='chat'),
        path('api/authentication/login/', SigninView.as_view()),
        path('api/authentication/', include('rest_framework.urls', namespace='rest_framework'), name='api'),
    ]
    if settings.CACHEOPS_ENABLED and False:
        patterns += [
            path('i18n.js', cache_page(86400, key_prefix='i18n.js?_dc=%s' % key)(JavaScriptCatalog.as_view()), name='i18n-js'),
            path('i18n.json', cache_page(86400, key_prefix='i18n.json?_dc=%s' % key)(JSONCatalog.as_view()), name='i18n-json'),
            path('reverse.js', cache_page(86400, key_prefix='reverse.js?_dc=%s' % key)(reverse.urls_js), name='reverse-js'),
            path('reverse.json', cache_page(86400, key_prefix='reverse.json?_dc=%s' % key)(reverse.urls_json), name='reverse-json'),
            re_path(r'favicon.ico', cache_page(86400, key_prefix='i18n.js?_dc=%s' % key)(logo), name='logo'),
            re_path(r'^favicon.(?P<dimen>[^/]+).ico', cache_page(86400, key_prefix='i18n.js?_dc=%s' % key)(logo), name='logo'),
        ]
    else:
        patterns += [
            path('i18n.js', JavaScriptCatalog.as_view(), name='i18n-js'),
            path('i18n.json', JSONCatalog.as_view(), name='i18n-json'),
            path('reverse.js', reverse.urls_js, name='reverse-js'),
            path('reverse.json', reverse.urls_json, name='reverse-json'),
            re_path(r'favicon.ico', logo, name='logo'),
            re_path(r'^favicon.(?P<dimen>[^/]+).ico', logo, name='logo'),
        ]
    if settings.DEBUG:
        patterns += [
            re_path(r'^media/(?P<path>.*)$', serve, dict(document_root=settings.MEDIA_ROOT, show_indexes=True, )),
        ]
        if 'rosetta' in settings.INSTALLED_APPS:
            patterns += [
                re_path(r'^locale/', include('rosetta.urls'), name='rosetta')
            ]
    else:
        patterns += [
            re_path(r'^media/(?P<path>.*)$', serve, dict(document_root=settings.MEDIA_ROOT, )),
        ]
    logger.debug('Modules %s', settings.INSTALLED_MODULE)
    for application in [application for application in settings.INSTALLED_MODULE if application not in [pattern.namespace for pattern in patterns if isinstance(pattern, URLResolver)]]:
        try:
            urls = import_module('%s.urls' % (application,))
            logger.debug('Application %s', application)
            if hasattr(urls, 'urlpatterns'):
                patterns.append(path('%s/' % (urls.app_name or application,), include('%s.urls' % (urls.app_name or application,)), name=urls.app_name or application))
                logger.debug('Auto urls %s.urls append', application)
            else:
                logger.debug('Auto urls %s.urls not contains urlpatterns', application)
        except Exception as e:
            logger.info(e)
    return patterns


urlpatterns = urlpatterns()
module = sys.modules[__name__]
setattr(module, 'handler400', views.BadRequest)
setattr(module, 'handler403', views.PermissionDenied)
setattr(module, 'handler404', views.PageNotFound)
setattr(module, 'handler500', views.ServerError)
if sys.stdin and sys.stdin.isatty():
    pass
else:
    from plyer import notification
    import os
    from datetime import datetime

    notification.notify(
        title=settings.PROJECT['NAME'],
        message=f'''Application running ... \nDate : {datetime.now().strftime('%a, %d %b %Y %H:%M:%S.%f')[:-3]}''',
        app_name=settings.PROJECT['NAME'],
        app_icon=os.path.join(settings.STATIC_ROOT, f'application/media/favicon.ico').replace('\\', '/') if os.path.exists(os.path.join(settings.STATIC_ROOT, f'application/media/favicon.ico')) else None,
        ticker=settings.PROJECT['NAME'],
    )
