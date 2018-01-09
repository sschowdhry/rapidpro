from __future__ import absolute_import, unicode_literals

import copy
import warnings

from dj_database_url import parse as db_url
from decouple import config

# Nyaruka settings.
from .settings_common import *  # noqa

# -----------------------------------------------------------------------------------
# Ilhasoft reimplementation of settings.py to follow 12factor app.
# By default all configurations assume the production environment.
# To change the behavior of app just create the respective envvar or create a .env
# file in the root of the project.
# -----------------------------------------------------------------------------------
# Code to get ngrok address dynamically
# resp = requests.get('http://localhost:4040/')
# for line in resp.text.split('\n'):
#      if 'ngrok.io' in line:
#          data = json.loads(line.split('JSON.parse(')[-1].split(');')[0])
#          data = json.JSONDecoder().decode(data)
#          pprint(data['Session']['Tunnels']['command_line']['URL'])
GDAL_LIBRARY_PATH = config('GDAL_LIBRARY_PATH', default='/usr/lib/libgdal.so.20')
GEOS_LIBRARY_PATH = config('GEOS_LIBRARY_PATH', default='/usr/lib/libgeos_c.so.1')

DEBUG_TOOLBAR = config('DEBUG_TOOLBAR', default=False, cast=bool)
DEBUG = config('DEBUG', default=False, cast=bool)

# -----------------------------------------------------------------------------------
# Used when creating callbacks for Twilio, Nexmo etc..
# -----------------------------------------------------------------------------------
HOSTNAME = config('HOSTNAME', default='localhost')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=lambda x: x.split())
SEND_MESSAGES = config('SEND_MESSAGES', default=True, cast=bool)
CELERY_ALWAYS_EAGER = config('CELERY_ALWAYS_EAGER', default=False, cast=bool)
IS_PROD = config('IS_PROD', default=True, cast=bool)  # This is really necessary? Why don't use DEBUG?
CELERY_EAGER_PROPAGATES_EXCEPTIONS = config('CELERY_EAGER_PROPAGATES_EXCEPTIONS', default=False, cast=bool)
BROKER_BACKEND = config('BROKER_BACKEND', default='redis')
BROKER_URL = config('BROKER_URL', default=BROKER_URL)
BRANDING['rapidpro.io']['link'] = 'https://{}'.format(HOSTNAME)
BRANDING['rapidpro.io']['api_link'] = 'https://{}'.format(HOSTNAME)
BRANDING['rapidpro.io']['docs_link'] = 'https://{}'.format(HOSTNAME)
BRANDING['rapidpro.io']['domain'] = '{}'.format(HOSTNAME)

# -----------------------------------------------------------------------------------
# Add a custom brand for development
# -----------------------------------------------------------------------------------

custom = copy.deepcopy(BRANDING['rapidpro.io'])
custom['name'] = 'Custom Brand'
custom['slug'] = 'custom'
custom['org'] = 'Custom'
custom['api_link'] = 'http://custom-brand.io'
custom['domain'] = 'custom-brand.io'
custom['email'] = 'join@custom-brand.io'
custom['support_email'] = 'support@custom-brand.io'
custom['allow_signups'] = True
BRANDING['custom-brand.io'] = custom

INSTALLED_APPS += ('lab', )

# -----------------------------------------------------------------------------------
# Redis & Cache Configuration (we expect a Redis instance on localhost)
# -----------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://%s:%s/%s" % (config('REDIS_HOST', REDIS_HOST),
                                          config('REDIS_PORT', REDIS_PORT),
                                          config('REDIS_DB', REDIS_DB)),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# -----------------------------------------------------------------------------------
# Need a PostgreSQL database on localhost with postgis extension installed.
# -----------------------------------------------------------------------------------
DATABASES = {
    'default': config('DATABASE_URL',
                      default='postgis://temba:temba@localhost/temba',
                      cast=db_url)
}
DATABASES['default']['ATOMIC_REQUESTS'] = True
DATABASES['direct'] = DATABASES['default'].copy()
DATABASES['default']['DISABLE_SERVER_SIDE_CURSORS'] = True

INTERNAL_IPS = ('127.0.0.1',)
MIDDLEWARE_CLASSES = ('temba.middleware.ExceptionMiddleware',) + MIDDLEWARE_CLASSES

# -----------------------------------------------------------------------------------
# Load development apps
# -----------------------------------------------------------------------------------
INSTALLED_APPS = INSTALLED_APPS + ('storages',)
if DEBUG_TOOLBAR:
    try:
        import debug_toolbar
        INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar', )
        MIDDLEWARE_CLASSES = ('debug_toolbar.middleware.DebugToolbarMiddleware',) + MIDDLEWARE_CLASSES
    except ImportError:
        warnings.warn('DEBUG mode is enabled, but debug_toolbar is not found.')

if DEBUG:
    try:
        import django_extensions
        INSTALLED_APPS = INSTALLED_APPS + ('django_extensions', )
    except ImportError:
        warnings.warn('DEBUG mode is enabled, but django_extensions is not found.')


# -----------------------------------------------------------------------------------
# This setting throws an exception if a naive datetime is used anywhere. (they should
# always contain a timezone)
# -----------------------------------------------------------------------------------
warnings.filterwarnings('error', r"DateTimeField .* received a naive datetime",
                        RuntimeWarning, r'django\.db\.models\.fields')

# -----------------------------------------------------------------------------------
# Make our sitestatic URL be our static URL on development
# -----------------------------------------------------------------------------------
STATIC_URL = '/sitestatic/'

MAGE_API_URL = config('MAGE_API_URL', default='http://mage:8026/api/v1')
MAGE_AUTH_TOKEN = config('MAGE_AUTH_TOKEN')