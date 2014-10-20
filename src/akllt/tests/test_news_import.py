# coding: utf-8
from __future__ import unicode_literals

import datetime
import unittest
import pkg_resources

import django.test
from django.core.management import call_command

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

        news_items = list(map(shorten_values, news))

        self.assertEqual(len(news_items), 2)
        self.assertEqual(len(news_items[0]), 9)
        self.assertEqual(news_items[0]['date'], datetime.date(2010, 3, 16))
        self.assertEqual(news_items[0]['email'], 'antanasb@gmail.com')
        self.assertEqual(news_items[0]['profesionalams'], False)
        self.assertEqual(news_items[0]['title'], 'Praktinis seminaras moky...')
        self.assertEqual(news_items[0]['author'], 'Antanas')
        self.assertEqual(news_items[0]['blurb'], '2010m. kovo 22 ir 26 die...')
        self.assertEqual(news_items[0]['body'], '<p>2010m. kovo 22 ir 26 ...')
        self.assertEqual(len(news_items[0]['categories']), 10)
        self.assertEqual(news_items[0]['categories'][0], 'Biuro programos')
        self.assertEqual(news_items[0]['categories'][1], 'OpenOffice')
        self.assertEqual(news_items[0]['categories'][2], 'Interneto programos')
        self.assertEqual(news_items[0]['categories'][3], 'Grafikos programos')
        self.assertEqual(news_items[0]['categories'][4], 'Multimedia')
        self.assertEqual(news_items[0]['categories'][5], 'Žaidimai ir pramogos')
        self.assertEqual(news_items[0]['categories'][6], 'Laisva PĮ Lietuvoje')
        self.assertEqual(news_items[0]['categories'][7], 'GNU/Linux OS')
        self.assertEqual(news_items[0]['categories'][8], 'GNOME aplinka')
        self.assertEqual(news_items[0]['categories'][9], 'Sėkmės istorijos')
        self.assertEqual(len(news_items[0]['category_values']), 18)
        self.assertEqual(news_items[0]['category_values'][0], 'Biuro programos')
        self.assertEqual(news_items[0]['category_values'][1], 'OpenOffice')
        self.assertEqual(news_items[0]['category_values'][2], 'Interneto programos')
        self.assertEqual(news_items[0]['category_values'][3], 'Grafikos programos')
        self.assertEqual(news_items[0]['category_values'][4], 'Multimedia')
        self.assertEqual(news_items[0]['category_values'][5], 'Žaidimai ir pramogos')
        self.assertEqual(news_items[0]['category_values'][6], 'Programavimas')
        self.assertEqual(news_items[0]['category_values'][7], 'Laisva PĮ Lietuvoje')
        self.assertEqual(news_items[0]['category_values'][8], 'Laisvi formatai ir standartai')
        self.assertEqual(news_items[0]['category_values'][9], 'GNU/Linux OS')
        self.assertEqual(news_items[0]['category_values'][10], 'GNU/Hurd OS')
        self.assertEqual(news_items[0]['category_values'][11], 'FreeBSD OS')
        self.assertEqual(news_items[0]['category_values'][12], 'OpenBSD OS')
        self.assertEqual(news_items[0]['category_values'][13], 'GNOME aplinka')
        self.assertEqual(news_items[0]['category_values'][14], 'KDE aplinka')
        self.assertEqual(news_items[0]['category_values'][15], 'Grafinės aplinkos')
        self.assertEqual(news_items[0]['category_values'][16], 'Sėkmės istorijos')
        self.assertEqual(news_items[0]['category_values'][17], 'Patentai ir autorinės teisės')
        self.assertEqual(news_items[1], {
            'date': datetime.date(2002, 10, 15),
            'title': 'Konkursas',
            'blurb': '<p>Vilniuje, dvi dienas ...',
            'body': '<p>Vilniuje, dvi dienas ...',
        })


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


class NewsImportCommandTests(django.test.TestCase):
    def test_command(self):
        self.assertEqual(NewsStory.objects.count(), 0)
        call_command(
            'akllt_importnews',
            pkg_resources.resource_filename(
                'akllt',
                'tests/fixtures/naujienos'
            )
        )
        self.assertEqual(NewsStory.objects.count(), 2)
