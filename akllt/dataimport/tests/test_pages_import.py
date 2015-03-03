from django.test import TestCase

from wagtail.wagtailcore.models import Site
from wagtail.wagtailcore.models import Page

from akllt.dataimport.wagtail import get_root_page
from akllt.dataimport.tests.utils import fixture
from akllt.dataimport.importers.base import ImportItem
from akllt.dataimport.importers.pages import PagesImporter
from akllt.dataimport.tests.utils import get_default_site


class PagesImporterTests(TestCase):
    def setUp(self):
        root = get_default_site().root_page
        self.importer = PagesImporter('Atviras kodas', 'ak')
        self.importer.set_up(root, fixture('whole_export'))

    def test_get_parent_page(self):
        self.importer.path /= 'ak'
        path = self.importer.path / 'atviri_standartai'
        url_paths = lambda: sorted(list(
            self.importer.root.get_descendants().
            values_list('url_path', flat=True)
        ))

        # Test situation when parent page does not exist
        self.importer.get_parent_page(path / 'atviri_standartai.zpt')
        self.assertEqual(url_paths(), ['/home/ak/atviri_standartai/'])

        # Test situation when parent page exists
        self.importer.get_parent_page(path / 'atviri_standartai.zpt')
        self.assertEqual(url_paths(), ['/home/ak/atviri_standartai/'])

    def test_iterate_paths(self):
        base = fixture('whole_export')
        paths = self.importer.iterate_paths()
        self.assertEqual(sorted([str(p.relative_to(base)) for p in paths]), [
            'ak/atviri_standartai.html',
            'ak/dokumentacija.html',
            'ak/free-sw.html',
            'ak/knygos.html',
            'ak/licencijos/copyleft.html',
            'ak/licencijos/gpl.html',
            'ak/licencijos/kategorijos.html',
            'ak/licencijos/lgpl.html',
            'ak/osd.html',
        ])

    def test_parse_metadata(self):
        item = ImportItem(path=self.importer.path)
        data = self.importer.parse_metadata(item)
        self.assertEqual(data, {
            'slug': 'ak',
            'date': None,
            'title': 'atviras kodas',
            'body': '',
        })

    def test_import(self):
        self.importer.import_all_items()
        root = get_root_page()
        pages = (
            Page.objects.descendant_of(root).values_list('url_path', 'title')
        )
        self.assertEqual(sorted(pages), [
            ('/home/ak/', 'Atviras kodas'),
            ('/home/ak/atviri_standartai/', 'Atviri standartai'),
            ('/home/ak/dokumentacija/', 'Dokumentacija'),
            ('/home/ak/free-sw/', 'Laisvoji programinė įranga'),
            ('/home/ak/knygos/', 'Knygos'),
            ('/home/ak/licencijos/', 'licencijos'),
            ('/home/ak/licencijos/copyleft/', 'Kas yra Copyleft?'),
            ('/home/ak/licencijos/gpl/', 'GNU viešoji licencija'),
            ('/home/ak/licencijos/kategorijos/', 'PĮ kategorijos'),
            ('/home/ak/licencijos/lgpl/', 'GNU laisvoji viešoji licencija'),
            ('/home/ak/osd/', 'Atvirojo kodo apibrėžimas'),
        ])
