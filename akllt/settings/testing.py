# pylint: disable=wildcard-import,unused-wildcard-import

from akllt.settings.development import *  # noqa

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
