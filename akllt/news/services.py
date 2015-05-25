from wagtail.wagtailcore.models import Site


def get_news_index_page():
    """Returns a parent page for all the news."""
    site = Site.objects.get(is_default_site=True)
    return site.root_page.get_children().get(slug='naujienos')
