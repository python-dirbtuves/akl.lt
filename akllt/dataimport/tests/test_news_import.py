# coding: utf-8
from __future__ import unicode_literals

import pathlib
import datetime
import unittest
import pkg_resources

from operator import itemgetter

import django.test
from django.core.management import call_command

import akllt.dataimport.news as newsparser
from akllt.news.models import NewsStory


def fixture(path):
    return pathlib.Path(pkg_resources.resource_filename(
        'akllt', 'dataimport/tests/fixtures/%s' % path
    ))


def shorten_values(item):
    shortened = {}
    for key, value in item.items():
        if isinstance(value, str) and len(value) > 24:
            shortened[key] = '%s...' % value[:24]
        else:
            shortened[key] = value
    return shortened


class NewsExportReadTests(unittest.TestCase):
    def setUp(self):
        self.news_dir = pkg_resources.resource_filename(
            'akllt', 'dataimport/tests/fixtures/naujienos'
        )

    def test_iter_news_files(self):
        news_items = newsparser.iter_news_files(self.news_dir)
        self.assertEqual(sorted([p.name for p in news_items]), [
            'naujiena_0001', 'naujiena_1016',
        ])

    def test_parse_metadata(self):
        files = newsparser.iter_news_files(self.news_dir)
        news_items = map(newsparser.parse_metadata, files)

        sort_by_url = itemgetter('url')
        news_items = sorted(map(shorten_values, news_items), key=sort_by_url)

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
        path = fixture('null_date_naujiena/naujiena_0183')
        news_item = newsparser.parse_metadata(path)
        self.assertIsNone(news_item['date'])


class NewsImportCommandTests(django.test.TestCase):
    def test_command(self):
        self.assertEqual(NewsStory.objects.count(), 0)
        call_command('akllt_importnews', fixture('naujienos'), verbosity=0)
        self.assertEqual(NewsStory.objects.count(), 2)
