import os
from drfapilogger.events import Events

if os.environ.get('RUN_MAIN', None) != 'true':
    default_app_config = 'drfapilogger.apps.LoggerConfig'

API_LOGGER_SIGNAL = Events()
