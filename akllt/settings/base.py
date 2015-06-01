"""
Django settings for akllt project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

from pathlib import Path
from django.conf import global_settings as defaults

PROJECT_DIR = Path(__file__).parents[2]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6*s1ia-oxj80hhj#^agy#ml3%2b(=nt*m2b3#dz=^chnh_*3^9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',
    'taggit',
    'modelcluster',
    'django_nose',
    'django_extensions',
    'django.contrib.admin',

    'wagtail.wagtailcore',
    'wagtail.wagtailadmin',
    'wagtail.wagtaildocs',
    'wagtail.wagtailsnippets',
    'wagtail.wagtailusers',
    'wagtail.wagtailimages',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsearch',
    'wagtail.wagtailredirects',
    'wagtail.wagtailforms',
    'wagtail.wagtailsites',

    'akllt.website',
    'akllt.homepage',
    'akllt.dataimport',
    'akllt.common',
    'akllt.news',
    'akllt.pages',
    'akllt.stub',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'akllt.website.middleware.LegacyRedirectMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = defaults.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'akllt.website.context_processors.debug',
)

ROOT_URLCONF = 'akllt.urls'

WSGI_APPLICATION = 'akllt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(PROJECT_DIR / 'var/db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'lt'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = str(PROJECT_DIR / 'var/www/media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_URL = '/static/'
STATIC_ROOT = str(PROJECT_DIR / 'var/www/static')

STATICFILES_DIRS = (
    str(PROJECT_DIR / 'parts/jquery'),
    str(PROJECT_DIR / 'parts/bootstrap'),
    str(PROJECT_DIR / 'parts/requirejs'),
)


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)


# django-ompressor settings
# https://pypi.python.org/pypi/django_compressor

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

# Auth settings
LOGIN_REDIRECT_URL = '/'


# Wagtail settings
WAGTAIL_SITE_NAME = 'Atviras Kodas Lietuvai'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'warnings': {
            '()': 'akllt.log.FilterWarnings',
        },
    },
    'formatters': {
        'stdout': {
            'format': (
                '%(levelname)s %(asctime)s %(module)s '
                '%(process)d %(thread)d %(message)s'
            ),
        },
        'console': {
            'format': '%(levelname)s %(module)s %(message)s',
        },
    },
    'handlers': {
        'stdout': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'stdout',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        'py.warnings': {
            'filters': ['warnings'],
        },
        'django': {
            'propagate': True,
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    }
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SOUTH_TESTS_MIGRATE = False

# django-allauth settings
TEMPLATE_CONTEXT_PROCESSORS += (
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

AKLLT_SORTED_AUTH_PROVIDERS = (
    'persona',
    'openid.google',
    'openid.yahoo',
)

SOCIALACCOUNT_PROVIDERS = {
    'persona': {
        'AUDIENCE': '127.0.0.1' if DEBUG else 'http://www.akl.lt',
        'REQUEST_PARAMETERS': {
            'siteName': 'AKL',
        },
    },
    'openid': {
        'SERVERS': [
            {
                'id': 'google',
                'name': 'Google',
                'openid_url': 'https://www.google.com/accounts/o8/id',
            },
            {
                'id': 'yahoo',
                'name': 'Yahoo',
                'openid_url': 'http://me.yahoo.com',
            },
        ],
    },
}

INSTALLED_APPS += (
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.persona',
    'allauth.socialaccount.providers.openid',
)


# Debug toolbar
INSTALLED_APPS += (
    'debug_toolbar',
)
INTERNAL_IPS = (
    '127.0.0.1',
)

INSTALLED_APPS += (
    'pylint_django',
)
