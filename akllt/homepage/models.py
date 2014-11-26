from wagtail.wagtailcore.models import Page

from akllt.news.models import NewsIndex
from akllt.news.models import NewsStory


class IndexPage(Page):
    def get_context(self, request, *args, **kwargs):
        news_index = NewsIndex.objects.get(slug='naujienos')
        return {
            'self': self,
            'request': request,
            'page_title': '',
            'news_items': (
                NewsStory.objects.live().descendant_of(news_index).
                order_by('-date')[:24]
            ),
        }
