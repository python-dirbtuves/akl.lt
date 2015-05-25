from django.conf.urls import patterns, url

from akllt.news.feeds import LatestNewsFeed
from akllt.news import views


urlpatterns = patterns(
    '',
    url(r'^feed/$', LatestNewsFeed(), name='rss'),
    url(r'^news/create/$', views.NewsStoryCreate.as_view(), name='news_create'),
)
