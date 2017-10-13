# Settings for live deployed environments: vagrant, staging, production, etc
from .base import *  # noqa
import logging.config


ENVIRONMENT = os.environ['ENVIRONMENT'].lower()

WEBSERVER_ROOT = '/var/www/hello_tequila/'

PUBLIC_ROOT = os.path.join(WEBSERVER_ROOT, 'public')

STATIC_ROOT = os.path.join(PUBLIC_ROOT, 'static')

MEDIA_ROOT = os.path.join(PUBLIC_ROOT, 'media')

# ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(';')
ALLOWED_HOSTS = [os.environ['DOMAIN']]

os.environ.setdefault('CACHE_HOST', '127.0.0.1:11211')
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '%(CACHE_HOST)s' % os.environ,
    }
}

DATABASES['default']['NAME'] = 'hello_tequila_%s' % ENVIRONMENT.lower()
DATABASES['default']['USER'] = 'hello_tequila_%s' % ENVIRONMENT.lower()
DATABASES['default']['HOST'] = os.environ.get('DB_HOST', '')
DATABASES['default']['PORT'] = os.environ.get('DB_PORT', '')
DATABASES['default']['PASSWORD'] = os.environ.get('DB_PASSWORD', '')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'basic': {
            'format': '%(asctime)s %(name)-20s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'basic',
            'filename': os.path.join(WEBSERVER_ROOT, 'log', 'hello_tequila.log'),
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 10,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'hello_tequila': {
            'handlers': ['file', 'mail_admins'],
            'level': 'INFO',
        },
        'django.security': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True
        },
    },
}
logging.config.dictConfig(LOGGING)

MEDIA_ROOT = os.path.join(PUBLIC_ROOT, 'media')

# SECRET_KEY = os.environ.get('SECRET_KEY', '')
SECRET_KEY = os.environ['SECRET_KEY']

CSRF_COOKIE_SECURE = True

# We serve many staging sites via URLs like project-staging.caktusgroup.com.
# Not all of these are set up to be secure, so this setting must be False.
SECURE_HSTS_INCLUDE_SUBDOMAINS = False

SECURE_HSTS_SECONDS = 31536000  # 1 year

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_SECURE = True

SITE_ID = os.environ['SITE_ID']

STATIC_ROOT = os.path.join(PUBLIC_ROOT, 'static')

DEBUG = False

EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', False)
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', False)
