import json
import os
import re as regex
import sys
from datetime import timedelta
from importlib import import_module
from pathlib import Path

import structlog
from django import get_version
from django.core.serializers.json import DjangoJSONEncoder
from django.db.backends.base.base import RAN_DB_VERSION_CHECK as SkipDatabaseVersionCheck

from core.utils import ShortUUID

try:
    from django.utils.translation import gettext_lazy as _
except:
    _ = lambda string: string

import library.yamlconfig as config
from core import constants

json.JSONEncoder.default = DjangoJSONEncoder.default
PROJECT = {
    'NAME': 'ERPro',
    'VERSION': ('1.0.0', _('Beta Release')),
    'SLOGAN': _('Enterprise ERP For Everyone'),
    'LOGO': '/application/media/erpro',
}
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = '3Zsn9x5hrKW6z54avxaQYZxvinfyttQxUhFasqPJMbm3VXXMDG9BL8Cjv6GRkw4AMKrXUKpeqbwG4AYPPA84DkPNHcEVCiHtsLhU'
SECRET_KEY_FALLBACKS = []
DEBUG = True
ALLOWED_HOSTS = [] if DEBUG else ['*', ]
INSTALLED_LIBRARY = [
    'core.patch',
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'whitenoise.runserver_nostatic',
    'channels',
    'library.commentmigrate',
    'library.yamlconfig',
    'library.simplehistory',
    'library.modelutils',
    'library.extensions',
    'library.corsheaders',
    'library.maintenancemode',
    'library.cacheops',
    'library.treebeard',
    'rest_framework',
    'library.restframeworkflexfields',
    'library.jsreverse',
    'library.revproxy',
    'library.djangohuey',
    'library.hueymonitorutils',
    'library.hueymonitor',
    'library.chatterbot.ext.django',
    'rosetta',
    'core.sql',
]
INSTALLED_MODULE = [
    'authentication',
]
INSTALLED_APPS = INSTALLED_LIBRARY + INSTALLED_MODULE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'library.corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'authentication.middleware.SesameMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'core.middleware.LocaleMiddleware',
    'core.middleware.TimezoneMiddleware',
    'core.middleware.IFrameOptionsMiddleware',
    'core.middleware.SessionThreadLocalMiddleware',
    'core.middleware.SessionTimeoutMiddleware',
    'core.middleware.MinifyMiddleware',
    'core.middleware.PostTunnelingMiddleware',
    'core.middleware.SearchContextMiddleware',
    'library.simplehistory.middleware.HistoryRequestMiddleware',
    'library.maintenancemode.middleware.MaintenanceModeMiddleware',
    'core.middleware.StructLogMiddleware',
    'core.middleware.ServerMiddleware',
]
ROOT_URLCONF = 'setup.urls'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    'APP_DIRS': False,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'core.processors.template',
        ],
        'loaders': [
            'core.loaders.DatabaseLoader',
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ],
    },
}, ]
TEMPLATES_USE_CODEMIRROR = True
ASGI_APPLICATION = 'setup.asgi.application'
DATABASES = {
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '{0}.sqlite3'.format(PROJECT['NAME'].lower())),
    },
    'postgres': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django.{0}'.format(PROJECT['NAME'].lower()),
        'USER': PROJECT['NAME'].lower(),
        'PASSWORD': PROJECT['NAME'].lower(),
        'HOST': '127.0.0.1',
        'PORT': 5432,
        'ATOMIC_REQUESTS': True,
    },
}
CHANNEL_LAYERS = {
    'memory': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
    'redis': {
        'BACKEND': 'library.channelsredis.pubsub.RedisPubSubChannelLayer',
        'CONFIG': {
            'hosts': ['redis://{user}:{password}@127.0.0.1:6379'.format(user=PROJECT['NAME'].lower(), password=PROJECT['NAME'].lower())],
            'symmetric_encryption_keys': [SECRET_KEY],
        },
    },
    'rabbitmq': {
        'BACKEND': 'library.channelsrabbitmq.core.RabbitmqChannelLayer',
        'CONFIG': {
            'host': 'amqp://{user}:{password}@127.0.0.1:5672'.format(user=PROJECT['NAME'].lower(), password=PROJECT['NAME'].lower()),
        },
    },
}
CHANNEL_MSGPACK = True
CACHES = {
    'dummy': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'cache.{0}.mem'.format(PROJECT['NAME'].lower()),
    },
    'memory': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'filebase': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'data', 'cache'),
    },
    'database': {
        'BACKEND': 'django.core.cache.backends.db.BaseDatabaseCache',
        'LOCATION': u'cache',
    },
    'redis': {
        'BACKEND': 'library.djangoredis.cache.RedisCache',
        'LOCATION': 'redis://{user}:{password}@127.0.0.1:6379'.format(user=PROJECT['NAME'].lower(), password=PROJECT['NAME'].lower()),
        'OPTIONS': {
            'CLIENT_CLASS': 'library.djangoredis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': False,
        },
        'KEY_PREFIX': 'cache',
    },
}
CACHEOPS_ENABLED = True
CACHEOPS_LRU = True
CACHEOPS_REDIS = CACHES['redis']['LOCATION']
CACHEOPS_DEFAULTS = {
    'timeout': 60 * 60,
}
CACHEOPS = {
    'authentication.*': {'ops': 'all'},
    'core.*': {'ops': 'all'},
    'comment.*': {'ops': ('fetch', 'all')},
    'migrations.*': None,
    'admin.*': None,
    'library.watson.*': None,
    'auth.*': None,
    'contenttypes.*': None,
    'hueymonitor.*': None,
    'sessions.*': None,
    '*.*': {},
}
CACHEOPS_DEGRADE_ON_FAILURE = True
CACHEOPS_PREFIX = lambda _: 'cacheops'
FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'setup', 'fixtures'),
)
AUTH_PASSWORD_VALIDATORS = [{
    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
}, {
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    'OPTIONS': {
        'min_length': 6,
    },
}, {
    'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
}, {
    'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
}, ]
LANGUAGE_CODE = 'id'
LANGUAGES = [(key, value,) for key, value, flag in constants.Languages]
LANGUAGE_COOKIE_NAME = '{0}language'.format(PROJECT['NAME'].lower())
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_THOUSAND_SEPARATOR = True
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]
USE_TZ = True
ROSETTA_MESSAGES_PER_PAGE = 15
ROSETTA_POFILE_WRAP_WIDTH = 0
ROSETTA_EXCLUDED_APPLICATIONS = tuple(INSTALLED_LIBRARY)
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
SITE_ID = 1659710928748
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = (
    'jpg',
    'jpeg',
    'png',
    'gif',
    'webp',
    'zip',
    'gz',
    'tgz',
    'bz2',
    'tbz',
    'xz',
    'br',
    'swf',
    'flv',
    'woff',
    'woff2',
    'ts',
    'less',
    'scss',
)
WHITENOISE_INDEX_FILE = True
WHITENOISE_MIMETYPES = {
    '.css': 'text/css',
    '.js': 'text/javascript',
}


def function(headers, path, url):
    from core.middleware import server
    headers['Content-Disposition'] = 'attachment'
    for key, header in server.headers().items():
        headers[key] = header


WHITENOISE_ADD_HEADERS_FUNCTION = lambda headers, path, url: function(headers, path, url)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTHENTICATION_BACKENDS = [
    'authentication.backends.SigninBackend',
    'authentication.backends.SesameBackend',
    'permission.backends.ObjectPermissionBackend',
]
AUTHENTICATION = {
    'CAPCHA': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
}
PERMISSION = {}
SESAME_TOKEN_NAME = 'magic'
SESAME_ONE_TIME = False
AUTH_USER_MODEL = 'authentication.User'
LOGIN_URL = '/authentication/signin/'
LOGIN_REDIRECT_URL = '/authentication/signin/'
LOGOUT_REDIRECT_URL = '/'
CSRF_RANDOM = False
CSRF_COOKIE_NAME = 'csrf'
CSRF_HEADER_NAME = f'HTTP_X_{CSRF_COOKIE_NAME.upper()}_TOKEN'
CSRF_TRUSTED_ORIGINS = []
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = []
CORS_ALLOW_HEADERS = []
SESSION_EXPIRE_SECONDS = 3600
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD = 60
SESSION_REMEMBER_PERIOD = 86400
SESSION_TIMEOUT_REDIRECT = '/authentication/unlock/'
ORGS_SLUGFIELD = 'library.extensions.db.fields.AutoSlugField'
MAINTENANCE_MODE = False
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'core.apis.exceptions.ExceptionHandler',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}
DRF_API_LOGGER_DATABASE = True
DRF_API_LOGGER_PATH_TYPE = 'FULL'
JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30, ),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1, ),
    'ROTATE_REFRESH_TOKENS': True,
    'UPDATE_LAST_LOGIN': True,
    'USER_ID_FIELD': 'user_id',
    'ALGORITHM': 'HS512',
    'AUDIENCE': '{0}.Mobile'.format(PROJECT['NAME']),
    'ISSUER': PROJECT['NAME'],
    'USER_ID_CLAIM': 'user',
    'TOKEN_TYPE_CLAIM': 'type',
}
COMPRESS_ENABLED = False
COMPRESS_OUTPUT_DIR = 'compressed'
WHATSAPP = {
    'PORT': 3333,
    'WEBHOOK_URL': 'http://127.0.0.1:8000/whatsapp/webhook/',
    'LOG_LEVEL': 'debug',
    'SESSION': os.path.join(BASE_DIR, 'data/whatsapp/'),
    'CONFIG': None,
}
CHATBOT = {
    'ENABLED': True,
    'READ_ONLY': True,
    'TRAINING': [],
}
DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440 * 4
COMMENT_MIGRATE_EXCLUDE_MODEL = []
MANAGE_CLEAR_CONSOLE = True
NUMBERING_PATTERN = r'a-zA-Z0-9.()@#:\[\]'
SECURE_SSL_REDIRECT = False
SIMPLE_HISTORY_HISTORY_ID_USE_UUID = False
SIMPLE_HISTORY_HISTORY_CHANGE_REASON_USE_TEXT_FIELD = True
HUEYS = {
    'default': 'low',
    'queues': {
        'low': {
            'huey_class': 'huey.PriorityRedisExpireHuey',
            'name': 'low',
            'results': True,
            'store_none': False,
            'immediate': False,
            'utc': True,
            'blocking': True,
            'consumer': {
                'workers': 1,
                'worker_type': 'thread',
                'initial_delay': 0.1,
                'backoff': 1.15,
                'max_delay': 10.0,
                'scheduler_interval': 1,
                'periodic': True,
                'check_worker_health': True,
                'health_check_interval': 1,
            },
        },
        'high': {
            'huey_class': 'huey.PriorityRedisExpireHuey',
            'name': 'high',
            'results': True,
            'store_none': False,
            'immediate': False,
            'utc': True,
            'blocking': True,
            'consumer': {
                'workers': 5,
                'worker_type': 'thread',
                'initial_delay': 0.1,
                'backoff': 1.15,
                'max_delay': 10.0,
                'scheduler_interval': 1,
                'periodic': True,
                'check_worker_health': True,
                'health_check_interval': 1,
            },
        },
    },
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            '()': structlog.stdlib.ProcessorFormatter,
            'fmt': '%(message)s',
            'processor': structlog.dev.ConsoleRenderer(force_colors=True, ),
            'foreign_pre_chain': [
                structlog.contextvars.merge_contextvars,
                structlog.processors.TimeStamper(fmt='iso', utc=False, ),
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.ExceptionPrettyPrinter(),
                structlog.processors.CallsiteParameterAdder({
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                }),
            ],
        },
        'json': {
            '()': structlog.stdlib.ProcessorFormatter,
            'processor': structlog.processors.JSONRenderer(),
            'foreign_pre_chain': [
                structlog.contextvars.merge_contextvars,
                structlog.processors.TimeStamper(fmt='iso', utc=False, ),
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.CallsiteParameterAdder({
                    structlog.processors.CallsiteParameter.PATHNAME,
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.MODULE,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                    structlog.processors.CallsiteParameter.THREAD,
                    structlog.processors.CallsiteParameter.THREAD_NAME,
                    structlog.processors.CallsiteParameter.PROCESS,
                    structlog.processors.CallsiteParameter.PROCESS_NAME,
                }),
            ],
        },
    },
    'filters': {
        'require.debug': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'filters': ['require.debug', ],
            'formatter': 'console',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'filters': ['require.debug', ],
            'formatter': 'json',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'data/log/erpro.json'),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 10,
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['default', ],
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['default', ],
    },
}
AUDITLOG_INCLUDE_ALL_MODELS = False

SkipDatabaseVersionCheck.clear()
settings = config.load(base_dir=BASE_DIR, project='erpro', )
from importlib.metadata import version
from core.settings import safesettings

safesettings()
settings.PROJECT.update(
    DJANGO=regex.sub(r'[^\d.]', '', get_version()),
    SERVER='Daphne',
    DAPHNE=regex.sub(r'[^\d.]', '', version('daphne')),
)
if any(item in [
    'uvicorn',
    'runuvicorn',
    'hypercorn',
    'runhypercorn',
] for item in sys.argv):
    setattr(settings, 'CHANNEL_MSGPACK', False)
if any(item in [
    'runserver',
] for item in sys.argv):
    setattr(settings, 'SECURE_SSL_REDIRECT', False)
if not os.path.exists(os.path.dirname(settings.LOGGING['handlers']['file']['filename'])):
    os.makedirs(os.path.dirname(settings.LOGGING['handlers']['file']['filename']))
for module in settings.INSTALLED_MODULE:
    if not os.path.exists(os.path.join(settings.BASE_DIR, module, 'fixtures')):
        os.makedirs(os.path.join(settings.BASE_DIR, module, 'fixtures'))
    if not os.path.exists(os.path.join(settings.BASE_DIR, module, 'locale')):
        os.makedirs(os.path.join(settings.BASE_DIR, module, 'locale'))
for alias, property in settings.DATABASES.items():
    if 'VERSION_CHECK' in property and not property.get('VERSION_CHECK', True):
        SkipDatabaseVersionCheck.add(alias)
settings.DATABASES.update(
    default=settings.DATABASES[getattr(settings, 'DATABASES_DEFAULT', 'sqlite')],
)
settings.CHANNEL_LAYERS.update(
    default=settings.CHANNEL_LAYERS[getattr(settings, 'CHANNEL_DEFAULT', 'memory')],
)
settings.CACHES.update(
    default=settings.CACHES[getattr(settings, 'CACHES_DEFAULT', 'dummy')],
)
setattr(settings, 'CACHEOPS_REDIS', settings.CACHES['redis']['LOCATION'])
for key, queue in settings.HUEYS['queues'].items():
    queue.update(url=settings.CACHES['redis']['LOCATION'], )
if not settings.DEBUG:
    setattr(settings, 'ALLOWED_HOSTS', settings.ALLOWED_HOSTS if len(settings.ALLOWED_HOSTS) > 0 else ['*'], )
    setattr(settings, 'CSRF_TRUSTED_ORIGINS', settings.CSRF_TRUSTED_ORIGINS if len(settings.CSRF_TRUSTED_ORIGINS) > 0 else [
        'http://{0}:80'.format(os.environ.get('LOCAL_ADDRESS')),
        'https://{0}:80'.format(os.environ.get('LOCAL_ADDRESS')),
    ], )
    if settings.CSRF_RANDOM:
        setattr(settings, 'CSRF_COOKIE_NAME', f'csrf{ShortUUID().random(length=10)}', )
        setattr(settings, 'CSRF_HEADER_NAME', f'HTTP_X_{settings.CSRF_COOKIE_NAME.upper()}_TOKEN', )
    settings.LOGGING['handlers']['default'].update(formatter='json', )
    settings.LOGGING['loggers']['django.db.backends'].update(
        level='ERROR',
        handlers=['default', 'file', ],
    )
    settings.LOGGING['root'].update(
        level='ERROR',
        handlers=['default', 'file', ],
    )
if any(item in [
    'migrate',
    'makemigrations',
    'showmigrations',
    'collecticon',
    'collectpermission',
    'dumpdata',
    'loaddata',
] for item in sys.argv):
    settings.LOGGING['loggers']['django.db.backends'].update(
        level='INFO',
        handlers=['default', ],
    )
if isinstance(settings.JWT['ACCESS_TOKEN_LIFETIME'], (str, int)):
    settings.JWT.update(ACCESS_TOKEN_LIFETIME=timedelta(seconds=int(eval(str(settings.JWT.get('ACCESS_TOKEN_LIFETIME', settings.SESSION_EXPIRE_SECONDS)))), ))
if isinstance(settings.JWT['REFRESH_TOKEN_LIFETIME'], (str, int)):
    settings.JWT.update(REFRESH_TOKEN_LIFETIME=timedelta(seconds=int(eval(str(settings.JWT.get('REFRESH_TOKEN_LIFETIME', settings.SESSION_REMEMBER_PERIOD)))), ))
for application in list(filter(lambda applications: os.path.isdir(applications) and os.path.exists(os.path.join(applications, 'apps.py')) and not os.path.exists(os.path.join(applications, '.disabled')), os.listdir(settings.BASE_DIR), )):
    def register(application):
        import logging
        logger = logging.getLogger(__name__)
        try:
            module = import_module('%s.%s' % (application, 'apps'))
            if hasattr(module, 'ApplicationConfig'):
                if hasattr(getattr(module, 'ApplicationConfig'), 'dependencies'):
                    for dependencie in list(filter(lambda dependencies: dependencies not in settings.INSTALLED_LIBRARY + settings.INSTALLED_MODULE, getattr(getattr(module, 'ApplicationConfig'), 'dependencies'))):
                        register(dependencie)
                if application not in settings.INSTALLED_LIBRARY + settings.INSTALLED_MODULE:
                    settings.INSTALLED_MODULE.append(application)
                    logger.debug('Auto apps %s.apps append', application)
        except Exception as e:
            logger.info(e)


    register(application)
setattr(settings, 'INSTALLED_APPS', settings.INSTALLED_LIBRARY + settings.INSTALLED_MODULE)
