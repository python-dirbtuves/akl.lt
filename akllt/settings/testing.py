# pylint: disable=wildcard-import,unused-wildcard-import
import os

from akllt.settings.development import *  # noqa

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
os.environ['RECAPTCHA_TESTING'] = 'True'
