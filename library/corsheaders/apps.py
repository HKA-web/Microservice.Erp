from __future__ import annotations

import logging
import sys

from django.apps import AppConfig
from django.core.checks import Tags, register

logger = logging.getLogger(__name__)


class CorsHeadersAppConfig(AppConfig):
    name = 'corsheaders'
    verbose_name = 'Cors Headers'

    def ready(self) -> None:
        from .checks import check_settings
        if not any(item in [
            'migrate',
            'makemigrations',
            'showmigrations',
            'makemessages',
            'compilemessages',
            'makelocale',
            'compilelocale',
        ] for item in sys.argv):
            logger.debug(f'Migration not detected, {self.name}.ready will Run')
            register(Tags.security)(check_settings)
        pass
