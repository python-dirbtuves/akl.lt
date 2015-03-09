import pathlib
import pkg_resources

from django.contrib.contenttypes.models import ContentType

from wagtail.wagtailcore.models import Site
from wagtail.wagtailcore.models import Page


def fixture(path):
    return pathlib.Path(pkg_resources.resource_filename(
        'akllt', 'dataimport/tests/fixtures/%s' % path
    ))


def wagtail_initial_data():
    """"Taken from wagtail/wagtailcore/migrations/0002_initial_data.py."""

    # Create page content type
    page_content_type, _ = ContentType.objects.get_or_create(
        model='page',
        app_label='wagtailcore',
        defaults={'name': 'page'}
    )

    # Create root page
    Page.objects.create(
        title="Root",
        slug='root',
        content_type=page_content_type,
        path='0001',
        depth=1,
        numchild=1,
        url_path='/',
    )

    # Create homepage
    homepage = Page.objects.create(
        title="Welcome to your new Wagtail site!",
        slug='home',
        content_type=page_content_type,
        path='00010001',
        depth=2,
        numchild=0,
        url_path='/home/',
    )

    # Create default site
    return Site.objects.create(
        hostname='localhost',
        root_page_id=homepage.id,
        is_default_site=True
    )


def get_default_site():
    try:
        return Site.objects.get(is_default_site=True)
    except Site.DoesNotExist:
        return wagtail_initial_data()
