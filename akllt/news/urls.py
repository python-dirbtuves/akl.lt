from django.conf.urls import patterns, url

urlpatterns = patterns(
    'akllt.news.views',
    url(r'^$', 'news_items', name='news_items'),
    url(
        r'news/(?P<slug>[a-z\d-]+)', 'news_item_details',
        name='news_item_details'
    ),
)
