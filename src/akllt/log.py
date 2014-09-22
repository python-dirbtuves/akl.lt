import logging


class FilterWarnings(logging.Filter):
    def filter(self, record):
        message = record.getMessage()
        if 'RemovedInDjango18Warning' in message:
            if 'treebeard' in message:
                return False
            if 'wagtail' in message:
                return False
            if 'django/forms/models.py' in message:
                return False
            if 'django/test/_doctest.py' in message:
                return False
        return True
