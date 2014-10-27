from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'akllt.news.views.news_items', name='news_items'),
)
