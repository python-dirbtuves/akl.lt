import datetime
import unittest
import pkg_resources

import django.test

from wagtail.wagtailcore.models import Page

from akllt.dataimport.news import import_news
from akllt.models import NewsStory


def shorten_values(item):
    shortened = {}
    for key, value in item.items():
        if isinstance(value, basestring) and len(value) > 24:
            shortened[key] = '%s...' % value[:24]
        else:
            shortened[key] = value
    return shortened


class NewsExportReadTests(unittest.TestCase):
    def test_iter_news(self):
        news_folder = pkg_resources.resource_filename(
            'akllt', 'tests/fixtures/naujienos'
        )
        news = import_news(news_folder)
        self.assertEqual(list(map(shorten_values, news)), [
            {
                'date': datetime.date(2002, 10, 15),
                'title': 'Konkursas',
                'blurb': '<p>Vilniuje, dvi dienas ...',
                'body': '<p>Vilniuje, dvi dienas ...',
            },
        ])


class NewsImportTests(django.test.TestCase):
    def test_create_news(self):
        self.assertEqual(NewsStory.objects.count(), 0)
        root = Page.add_root(title='Root page')

        news_folder = pkg_resources.resource_filename(
            'akllt', 'tests/fixtures/naujienos'
        )
        news = import_news(news_folder)
        for news_story in news:
            root.add_child(instance=NewsStory(
                title=news_story['title'],
                date=news_story['date'],
                blurb=news_story['blurb'],
                body=news_story['body'],
            ))
