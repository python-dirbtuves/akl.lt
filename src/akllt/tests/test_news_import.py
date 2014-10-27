# coding: utf-8
from __future__ import unicode_literals

import datetime
import unittest
import pkg_resources

from operator import itemgetter

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

        news_items = sorted(map(shorten_values, news), key=itemgetter('url'))

        eq = self.assertEqual

        eq(len(news_items), 2)

        eq(news_items[0], {
            'date': datetime.date(2002, 10, 15),
            'title': 'Konkursas',
            'blurb': '<p>Vilniuje, dvi dienas ...',
            'body': '<p>Vilniuje, dvi dienas ...',
            'url': 'naujiena_0001',
        })

        eq(len(news_items[1]), 10)
        eq(news_items[1]['date'], datetime.date(2010, 3, 16))
        eq(news_items[1]['email'], 'antanasb@gmail.com')
        eq(news_items[1]['profesionalams'], False)
        eq(news_items[1]['title'], 'Praktinis seminaras moky...')
        eq(news_items[1]['author'], 'Antanas')
        eq(news_items[1]['blurb'], '2010m. kovo 22 ir 26 die...')
        eq(news_items[1]['body'], '<p>2010m. kovo 22 ir 26 ...')
        eq(len(news_items[1]['categories']), 10)
        eq(news_items[1]['categories'][0], 'Biuro programos')
        eq(news_items[1]['categories'][1], 'OpenOffice')
        eq(news_items[1]['categories'][2], 'Interneto programos')
        eq(news_items[1]['categories'][3], 'Grafikos programos')
        eq(news_items[1]['categories'][4], 'Multimedia')
        eq(news_items[1]['categories'][5], 'Žaidimai ir pramogos')
        eq(news_items[1]['categories'][6], 'Laisva PĮ Lietuvoje')
        eq(news_items[1]['categories'][7], 'GNU/Linux OS')
        eq(news_items[1]['categories'][8], 'GNOME aplinka')
        eq(news_items[1]['categories'][9], 'Sėkmės istorijos')
        eq(len(news_items[1]['category_values']), 18)
        eq(news_items[1]['category_values'][0], 'Biuro programos')
        eq(news_items[1]['category_values'][1], 'OpenOffice')
        eq(news_items[1]['category_values'][2], 'Interneto programos')
        eq(news_items[1]['category_values'][3], 'Grafikos programos')
        eq(news_items[1]['category_values'][4], 'Multimedia')
        eq(news_items[1]['category_values'][5], 'Žaidimai ir pramogos')
        eq(news_items[1]['category_values'][6], 'Programavimas')
        eq(news_items[1]['category_values'][7], 'Laisva PĮ Lietuvoje')
        eq(
            news_items[1]['category_values'][8],
            'Laisvi formatai ir standartai'
        )
        eq(news_items[1]['category_values'][9], 'GNU/Linux OS')
        eq(news_items[1]['category_values'][10], 'GNU/Hurd OS')
        eq(news_items[1]['category_values'][11], 'FreeBSD OS')
        eq(news_items[1]['category_values'][12], 'OpenBSD OS')
        eq(news_items[1]['category_values'][13], 'GNOME aplinka')
        eq(news_items[1]['category_values'][14], 'KDE aplinka')
        eq(news_items[1]['category_values'][15], 'Grafinės aplinkos')
        eq(news_items[1]['category_values'][16], 'Sėkmės istorijos')
        eq(
            news_items[1]['category_values'][17],
            'Patentai ir autorinės teisės'
        )

    def test_null_date(self):
        news_folder = pkg_resources.resource_filename(
            'akllt', 'tests/fixtures/null_date_naujiena'
        )
        news_items = list(import_news(news_folder))

        self.assertIsNone(news_items[0]['date'])


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
