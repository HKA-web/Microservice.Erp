import logging
from importlib import import_module

from django.conf import settings

logger = logging.getLogger(__name__)


def websocket_urlpatterns():
    websocket_urlpatterns = []
    for application in settings.INSTALLED_MODULE:
        try:
            routings = import_module('%s.routings' % (application,))
            if hasattr(routings, 'websocket_urlpatterns'):
                websocket_urlpatterns += getattr(routings, 'websocket_urlpatterns')
                logger.debug('Auto routings %s append', routings.__name__)
        except Exception as e:
            logger.info(e)
    return websocket_urlpatterns
