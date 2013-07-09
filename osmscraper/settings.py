import os
import django
# calculated paths for django and the site
# used as starting points for various other paths
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT = '/'.join(SITE_ROOT.split('/')[:-1])

# Django settings for osmscraper project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG
APPEND_SLASH = False

ADMINS = (
    ('Ahmed Boussadia', 'ahmed@dalliz.com'),
)

ALLOWED_HOSTS =['127.0.0.1', '192.168.0.13', 'www.dalliz.com', 'mastercourses.cloudapp.net','dalliz.cloudapp.net', 'dalliz-dev.cloudapp.net','www.mastercourses.com', 'dev.mastercourses.com']

MANAGERS = ADMINS

import dj_database_url

if DEBUG:
	DATABASES = {
    	'default': dj_database_url.config(default='postgres://postgres:2asefthukom,3@localhost:5432/osmsdb'),
	}
else:
	DATABASES = {
	'default': dj_database_url.config(default='postgres://postgres:2asefthukom,3@mastercourses-db.cloudapp.net:5432/osmsdb'),
	}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # os.path.join(SITE_ROOT, 'static'),
    '/'.join([PROJECT_ROOT, 'dalliz', 'static']),
    '/'.join([PROJECT_ROOT, 'apps/backoffice/categories_matcher', 'static']),
    '/'.join([PROJECT_ROOT, 'apps/backoffice/categories_builder', 'static']),
    '/'.join([PROJECT_ROOT, 'apps/backoffice/brand_builder', 'static']),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '5*zoh*f8&amp;t0cr!lb0o77c8w8f69t!kzmgbwk6s^4tirm8@^poe'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


# Custom authentication backend
AUTHENTICATION_BACKENDS = (
    'apps.accounts.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend'
)

ROOT_URLCONF = 'osmscraper.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'osmscraper.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    # Third party apps
    'gunicorn',
    'kombu.transport.django',
    'djcelery',
    'south',
    'storages',
    'cachebuster',
    'haystack',
    'libs.pystache',
    'libs.soupselect',
    'rest_framework',

    # Home made apps
    'apps.api',
    'apps.scrapers',
    'apps.backoffice.categories_matcher',
    'apps.backoffice.categories_builder',
    'apps.backoffice.brand_builder',
    'apps.backoffice.brand_matcher',
    'apps.matcher',
    'apps.tags',
    'auchan',
    'monoprix',
    'ooshop',
    'dalliz',
    'cart',
    'mturk',
    'apps.frontend',

    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# Backend with Celery
# BROKER_BACKEND = 'django'
BROKER_URL = 'amqp://ahmed:2asefthukom,rabbit3@localhost:5672/myvhost'
CELERYD_MAX_TASKS_PER_CHILD = 4
CELERYD_TASK_TIME_LIMIT = 86400*7
CELERYD_TASK_SOFT_TIME_LIMIT = 86400*7
import djcelery
djcelery.setup_loader()


# S3 Storage for static files (production environnement)
AWS_ACCESS_KEY_ID = 'AKIAIGSH7FB6CXL277VQ'
AWS_SECRET_ACCESS_KEY = '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'
SANDBOX = False

if SANDBOX:
    HOST = 'mechanicalturk.sandbox.amazonaws.com'
else:
    HOST = 'mechanicalturk.amazonaws.com'

# Cache busting
from django.template.loader import add_to_builtins
# from cachebuster.detectors import git

add_to_builtins('cachebuster.templatetags.cachebuster')
# CACHEBUSTER_UNIQUE_STRING = git.unique_string(__file__)
CACHEBUSTER_PREPEND_STATIC = False

# Email configuration
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'hello@dalliz.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = 'MaBaAb12!hello'

# Memcachier configuration
def get_cache():
  try:
    os.environ['MEMCACHE_SERVERS'] = os.environ['MEMCACHIER_SERVERS']
    os.environ['MEMCACHE_USERNAME'] = os.environ['MEMCACHIER_USERNAME']
    os.environ['MEMCACHE_PASSWORD'] = os.environ['MEMCACHIER_PASSWORD']
    return {
      'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': os.environ['MEMCACHIER_SERVERS'],
        'TIMEOUT': 500,
        'BINARY': True,
      }
    }
  except:
    return {
      'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
      }
    }

CACHES = get_cache()


# Haystack configuration
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'mastercourses',
        'TIMEOUT': 60,
    },
}  
