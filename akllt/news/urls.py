from django.conf.urls import patterns, url

from akllt.news.feeds import LatestNewsFeed


urlpatterns = patterns(
    '',
    url(r'^feed/$', LatestNewsFeed(), name='rss'),
)
