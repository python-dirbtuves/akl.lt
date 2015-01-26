from wagtail.wagtailcore.models import Site
from wagtail.wagtailcore.models import Page

from akllt.dataimport.exceptions import ImporterError


def get_root_page():
    try:
        return Site.objects.get(is_default_site=True).root_page
    except Page.DoesNotExist:
        raise ImporterError('Can\'t find Wagtail root page.')
