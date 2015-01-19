# coding: utf-8
from __future__ import unicode_literals

import datetime

from operator import itemgetter

from django.test import TestCase
from wagtail.wagtailcore.models import Site
from wagtail.wagtailcore.models import Page

from akllt.dataimport.importmanager import ImportManager
from akllt.dataimport.importers.base import ImportItem
from akllt.dataimport.importers.news import NewsImporter
from akllt.dataimport.tests.utils import fixture


def shorten_values(item):
    shortened = {}
    for key, value in item.items():
        if isinstance(value, str) and len(value) > 24:
            shortened[key] = '%s...' % value[:24]
        else:
            shortened[key] = value
    return shortened


class NewsExportReadTests(TestCase):
    def test_iter_news_files(self):
        importer = NewsImporter('Naujienos', 'naujienos')
        importer.path = importer.get_path(fixture(''))
        paths = importer.iterate_paths()
        self.assertEqual(sorted([p.name for p in paths]), [
            'naujiena_0001', 'naujiena_1016',
        ])

    def test_parse_metadata(self):
        importer = NewsImporter('Naujienos', 'naujienos')
        importer.path = importer.get_path(fixture(''))
        items = importer.iterate_items()
        data = map(importer.parse_metadata, items)
        data = sorted(map(shorten_values, data), key=itemgetter('url'))

        eq = self.assertEqual

        eq(len(data), 2)

        eq(data[0], {
            'date': datetime.date(2002, 10, 15),
            'title': 'Konkursas',
            'blurb': '<p>Vilniuje, dvi dienas ...',
            'body': '<p>Vilniuje, dvi dienas ...',
            'url': 'naujiena_0001',
        })

        eq(len(data[1]), 10)
        eq(data[1]['date'], datetime.date(2010, 3, 16))
        eq(data[1]['email'], 'antanasb@gmail.com')
        eq(data[1]['profesionalams'], False)
        eq(data[1]['title'], 'Praktinis seminaras moky...')
        eq(data[1]['author'], 'Antanas')
        eq(data[1]['blurb'], '2010m. kovo 22 ir 26 die...')
        eq(data[1]['body'], '<p>2010m. kovo 22 ir 26 ...')
        eq(len(data[1]['categories']), 10)
        eq(data[1]['categories'][0], 'Biuro programos')
        eq(data[1]['categories'][1], 'OpenOffice')
        eq(data[1]['categories'][2], 'Interneto programos')
        eq(data[1]['categories'][3], 'Grafikos programos')
        eq(data[1]['categories'][4], 'Multimedia')
        eq(data[1]['categories'][5], 'Žaidimai ir pramogos')
        eq(data[1]['categories'][6], 'Laisva PĮ Lietuvoje')
        eq(data[1]['categories'][7], 'GNU/Linux OS')
        eq(data[1]['categories'][8], 'GNOME aplinka')
        eq(data[1]['categories'][9], 'Sėkmės istorijos')
        eq(len(data[1]['category_values']), 18)
        eq(data[1]['category_values'][0], 'Biuro programos')
        eq(data[1]['category_values'][1], 'OpenOffice')
        eq(data[1]['category_values'][2], 'Interneto programos')
        eq(data[1]['category_values'][3], 'Grafikos programos')
        eq(data[1]['category_values'][4], 'Multimedia')
        eq(data[1]['category_values'][5], 'Žaidimai ir pramogos')
        eq(data[1]['category_values'][6], 'Programavimas')
        eq(data[1]['category_values'][7], 'Laisva PĮ Lietuvoje')
        eq(
            data[1]['category_values'][8],
            'Laisvi formatai ir standartai'
        )
        eq(data[1]['category_values'][9], 'GNU/Linux OS')
        eq(data[1]['category_values'][10], 'GNU/Hurd OS')
        eq(data[1]['category_values'][11], 'FreeBSD OS')
        eq(data[1]['category_values'][12], 'OpenBSD OS')
        eq(data[1]['category_values'][13], 'GNOME aplinka')
        eq(data[1]['category_values'][14], 'KDE aplinka')
        eq(data[1]['category_values'][15], 'Grafinės aplinkos')
        eq(data[1]['category_values'][16], 'Sėkmės istorijos')
        eq(
            data[1]['category_values'][17],
            'Patentai ir autorinės teisės'
        )

    def test_null_date(self):
        importer = NewsImporter('Naujienos', 'naujienos')
        path = fixture('null_date_naujiena/naujiena_0183')
        data = importer.parse_metadata(ImportItem(path=path))
        self.assertIsNone(data['date'])

    def test_duplicates(self):
        data = {
            'date': datetime.date(2002, 10, 15),
            'title': 'Konkursas',
            'blurb': '<p>Vilniuje, dvi dienas ...',
            'body': '<p>Vilniuje, dvi dienas ...',
            'url': 'naujiena_0001',
        }

        root = Site.objects.get(is_default_site=True).root_page
        importer = NewsImporter('Naujienos', 'naujienos')
        importer.root = importer.get_root_page(root)

        inst_1, created_1 = importer.import_item(root, data)
        self.assertTrue(created_1)

        inst_2, created_2 = importer.import_item(root, data)
        self.assertFalse(created_2)

        self.assertEqual(inst_1.pk, inst_2.pk)

    def test_manager(self):
        export_dir = fixture('')
        root = Site.objects.get(is_default_site=True).root_page
        manager = ImportManager(root, export_dir)
        manager.add_importers([NewsImporter('Naujienos', 'naujienos')])
        for importer, item in manager.iterate():
            importer.import_(item)

        slugs = Page.objects.order_by('slug').values_list('slug', flat=True)
        self.assertEqual(list(slugs), [
            'home', 'naujiena_0001', 'naujiena_1016', 'root',
        ])

        page = Page.objects.get(slug='naujiena_0001')
        self.assertEqual(page.title, 'Konkursas')
