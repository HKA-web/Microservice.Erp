import logging
import sys

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class CacheopsConfig(AppConfig):
    name = 'cacheops'
    verbose_name = _('Cacheops')

    def ready(self):
        if not any(item in ('migrate', 'makemigrations', 'showmigrations', 'makemessages', 'compilemessages', 'makelocale', 'compilelocale', 'collectstatic', 'collectasset', 'dumpdata', 'loaddata', 'shell', '--mode=client',) for item in sys.argv):
            logger.debug(f'Migration not detected, {self.name}.ready will Run')
            from .query import install_cacheops
            from .transaction import install_cacheops_transaction_support
            install_cacheops()
            install_cacheops_transaction_support()
        pass
