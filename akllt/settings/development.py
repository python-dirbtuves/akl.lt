# pylint: disable=wildcard-import,unused-wildcard-import

from akllt.settings.base import *  # noqa

DEFAULT_FROM_EMAIL = 'development@akl.lt'

MODERATORS = (('Albertas', 'albertasgim@gmail.com'))

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

EMAIL_FILE_PATH = str(PROJECT_DIR / 'var/email')

SITE_URL = 'akl.lt'
