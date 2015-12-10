"""Common settings and globals."""


from os.path import abspath, basename, dirname, join, normpath
from sys import path
from environ import Env
gettext = _ = lambda s: s

########## PATH CONFIGURATION
PACKAGE_PATH = dirname(dirname(abspath(__file__)))
PACKAGE_NAME = basename(PACKAGE_PATH)

PROJECT_PATH = dirname(PACKAGE_PATH)
PROJECT_NAME = "OpenAID" or PACKAGE_NAME
PROJECT_PACKAGE = "openaid" or PACKAGE_NAME

REPO_PATH = dirname(PROJECT_PATH)
REPO_NAME = "open-aid" or basename(REPO_PATH)

CONFIG_DIR = 'config'
CONFIG_PATH = join(REPO_PATH, CONFIG_DIR)

RESOURCE_DIR = 'resources'
RESOURCES_PATH = join(REPO_PATH, RESOURCE_DIR)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(PROJECT_PATH)

# load environment variables
Env.read_env(normpath(join(CONFIG_PATH, '.env')))
env = Env()
########## END PATH CONFIGURATION


########## OPENAID CONFIGURATION
EARLYBIRD_ENABLE = env.bool('EARLYBIRD_ENABLE', True)

########## MAINTENANCE : maked the WORK IN PROGRESS PAGE appear on every page of the site
MAINTENANCE = env.bool('MAINTENANCE', False)
########## INSTANCE TYPE (DEVELOPMENT/STAGING/PRODUCTION)
INSTANCE_TYPE = env.str('INSTANCE_TYPE', "development")

OPENAID_CRS_DONOR = 6 # Italy
OPENAID_DSD_FILE = join(RESOURCES_PATH, 'crs', 'dsd.xml')
OPENAID_MULTIPLIER = 1000000.0
OPENAID_CURRENCY = 918 # EUR

TOP_ELEMENTS_NUMBER = 30

# USD-EUR
OPENAID_CURRENCY_CONVERSIONS = {
    2004: 0.8049,
    2005: 0.8046,
    2006: 0.7967,
    2007: 0.7305,
    2008: 0.6933,
    2009: 0.7181,
    2010: 0.755,
    2011: 0.7192,
    2012: 0.778,
    2014: 0.7537,
}

# purpose codes to be excluded when querying for Most important initiatives in DB (recipient page, etc)
OPENAID_INITIATIVE_PURPOSE_EXCLUDED = ['91010','93010']


ADDTHIS_PROFILE = 'ra-53be8c5b31fee67d'
########## END OPENAID CONFIGURATION


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DEBUG', False)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('admin', 'openaid-dev@depp.it'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# See: https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = "no-reply@openaid.esteri.it"
########## END MANAGER CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': env.db(),
}
########## END DATABASE CONFIGURATION


########## GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'Europe/Rome'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-US'
LANG_CODE = LANGUAGE_CODE[:2]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = (
    PACKAGE_PATH,
    join(PROJECT_PATH, "blog"),
    join(PROJECT_PATH, "faq"),
)
########## END GENERAL CONFIGURATION


########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(RESOURCES_PATH, 'media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(RESOURCES_PATH, 'static'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    normpath(join(PACKAGE_PATH, 'static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
########## END STATIC FILE CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env('SECRET_KEY')
########## END SECRET CONFIGURATION

########## SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []
########## END SITE CONFIGURATION


########## FIXTURE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    normpath(join(RESOURCES_PATH, 'fixtures')),
)
########## END FIXTURE CONFIGURATION


########## TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    # openaid contexts
    'openaid.contexts.project_context',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = (
    normpath(join(PACKAGE_PATH, 'templates')),
)
########## END TEMPLATE CONFIGURATION


########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    # Default Django middleware.
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # openaid earlybird middleware
    'openaid.middlewares.PrivateBetaMiddleware'
)
########## END MIDDLEWARE CONFIGURATION


########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % PACKAGE_NAME
########## END URL CONFIGURATION


########## APP CONFIGURATION
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sitemaps',

    # If you want to use the admin integration, modeltranslation must be put before django.contrib.admin.
    # see: https://django-modeltranslation.readthedocs.org/en/latest/installation.html#installed-apps
    'modeltranslation', # model field translations

    # Admin panel and documentation:
    'django.contrib.admin',
    # 'django.contrib.admindocs',

    # Django helper
    'django_extensions', # django helpers
    'iconfonts.django', # icon renderer
    'idioticon', # term glossary
    'mptt', # tree structure for models

    # third party apps
    'tinymce',
    'bootstrap_pagination',
    'django_mptt_admin', # admin
    'rest_framework', # api
    'django_select2',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'openaid',
    'openaid.codelists',
    'openaid.projects',
    'openaid.pages',
    'openaid.attachments',
    'tagging',
    'blog',
    'faq',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS
########## END APP CONFIGURATION


########## AUTHENTICATION CONFIGURATION
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)
########## END AUTHENTICATION CONFIGURATION


########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s.%(msecs).03d] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
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
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': normpath(join(RESOURCES_PATH, 'logs', 'openaid.log')),
            'formatter': 'verbose'
        },
        'management_logfile': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': normpath(join(RESOURCES_PATH, 'logs', 'management.log')),
            'mode': 'w',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'management': {
            'handlers': ['console', 'management_logfile'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'openaid': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
########## END LOGGING CONFIGURATION


########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = '%s.wsgi.application' % PACKAGE_NAME
########## END WSGI CONFIGURATION


########## SOUTH CONFIGURATION
# See: http://south.readthedocs.org/en/latest/installation.html#configuring-your-django-installation
INSTALLED_APPS += (
    # Database migration helpers:
    'south',
)
# Don't need to use South when setting up a test database.
SOUTH_TESTS_MIGRATE = False
########## END SOUTH CONFIGURATION


########## DJANGO-MODELTRANSLATION CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#languages
LANGUAGES = (
    ('en', _('English')),
    ('it', _('Italian')),
)
########## END DJANGO-MODELTRANSLATION CONFIGURATION


########## ICONFONTS CONFIGURATION
ICONFONT = 'font-awesome'
########## END ICONFONTS CONFIGURATION


########## DJANGO-HAYSTACK CONFIGURATION
INSTALLED_APPS += (
    'haystack',
)
SOLR_BASE_URL = env.str('SOLR_BASE_URL', default='http://127.0.0.1:8080/solr/open-aid-{lang}')


def solr_url(lang):
    return {
        'ENGINE': 'openaid.backends.MultilingualSolrEngine',
        'URL': SOLR_BASE_URL.format(lang=lang),
    }
HAYSTACK_CONNECTIONS = {
    'default': solr_url(LANG_CODE),
}
HAYSTACK_CONNECTIONS.update(dict([
    ('default_%s' % lang, solr_url(lang)) for lang, __ in LANGUAGES if lang != LANG_CODE
]))
########## END DJANGO-HAYSTACK CONFIGURATION

########## REST FRAMEWORK CONFIGURATION
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.JSONPRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '12/minute',  # 1 req every 5 seconds
        'user': '2/second',  # un-throttled  (default: '1/second')
    },
    'PAGINATE_BY': 25,
    'MAX_PAGE_BY': 500,
    'PAGINATE_BY_PARAM': 'page_size',
}
########## END REST FRAMEWORK CONFIGURATION

