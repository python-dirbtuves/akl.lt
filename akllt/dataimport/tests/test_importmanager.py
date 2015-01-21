from django.test import TestCase

from wagtail.wagtailcore.models import Site

from akllt.dataimport.importmanager import ImportManager
from akllt.dataimport.importers.news import NewsImporter
from akllt.dataimport.importers.pages import PagesImporter
from akllt.dataimport.tests.utils import fixture


class ImportManagerTests(TestCase):
    def test_get_total(self):
        root = Site.objects.get(is_default_site=True).root_page
        manager = ImportManager(root, fixture('whole_export'))
        manager.add_importers([
            NewsImporter('Naujienos', 'naujienos'),
            PagesImporter('Atviras kodas', 'ak'),
        ])
        self.assertEqual(manager.get_total(), 11)
