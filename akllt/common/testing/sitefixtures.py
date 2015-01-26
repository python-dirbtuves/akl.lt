from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.models import Site

from akllt.news.models import NewsIndex
from akllt.homepage.models import IndexPage


def set_up_site():
    # Set up page hierarchy
    root = Page.objects.get(url_path='/')
    index_page = root.add_child(instance=IndexPage(
        title='AKL',
        url_path='/',
        slug='index',
    ))
    index_page.add_child(instance=NewsIndex(
        title='Naujienos',
        url_path='/naujienos',
        slug='naujienos',
    ))

    # Set our index_page as site's root page
    site = Site.objects.get(is_default_site=True)
    site.root_page = index_page
    site.save()

    return site
