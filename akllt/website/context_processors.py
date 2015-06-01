from django.conf import settings


def debug(request):
    # pylint: disable=unused-argument
    return {'DEBUG': settings.DEBUG}
