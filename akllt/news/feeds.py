from django.contrib.syndication.views import Feed

from wagtail.wagtailcore.rich_text import expand_db_html

from akllt.news.models import NewsStory


class LatestNewsFeed(Feed):
    title = "Atviras kodas Lietuvai latest news"
    link = "http://akl.lt"
    description = "Atviras kodas Lietuvai latest news"

    def items(self):
        return NewsStory.objects.order_by('-date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return expand_db_html(item.body)
