# pylint: disable=wildcard-import,unused-wildcard-import

from akllt.settings.base import *  # noqa

DEBUG = False

ALLOWED_HOSTS = ['akl.lt', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'akllt',
        'USER': 'akl',
    }
}

LOGGING['root'] = {
    'level': 'WARNING',
    'handlers': ['stdout'],
}
