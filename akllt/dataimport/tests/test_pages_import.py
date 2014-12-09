from django.test import TestCase

from wagtail.wagtailcore.models import Site
from wagtail.wagtailcore.models import Page

from akllt.dataimport.tests.utils import fixture
from akllt.dataimport.importers.base import ImportItem
from akllt.dataimport.importers.pages import PagesImporter


class PagesImporterTests(TestCase):
    def setUp(self):
        root = Site.objects.get(is_default_site=True).root_page
        self.importer = PagesImporter('Atviras kodas', 'ak')
        self.importer.set_up(root, fixture('whole_export'))

    def test_iterate_paths(self):
        base = fixture('whole_export')
        paths = self.importer.iterate_paths()
        self.assertEqual(sorted([str(p.relative_to(base)) for p in paths]), [
            'ak',
            'ak/atviri_standartai',
            'ak/atviri_standartai.html',
            'ak/atviri_standartai/atviri_standartai.zpt',
        ])

    def test_parse_metadata(self):
        item = ImportItem(path=self.importer.path)
        data = self.importer.parse_metadata(item)
        self.assertEqual(data, {
            'url': 'ak',
            'date': None,
            'title': 'atviras kodas',
            'body': '',
        })

    def test_import(self):
        for item in self.importer.iterate_items():
            self.importer.import_(item)

        pages = Page.objects.values_list('url_path', flat=True)
        self.assertEqual(list(pages), [
            '/',
            '/home/',
            '/home/ak/',
            '/home/atviri_standartai/',
            '/home/atviri_standartai.html/',
            '/home/atviri_standartai.zpt/',
        ])
