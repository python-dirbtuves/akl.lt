import unittest

from django.test import TestCase

from wagtail.wagtailcore.models import Site
from wagtail.wagtailimages.models import Image

from akllt.dataimport.importmanager import ImportManager
from akllt.dataimport.importers.pages import PagesImporter
from akllt.dataimport.tests.utils import fixture


class ImportImageTests(TestCase):
    @unittest.skip('TODO')
    def test_import_image(self):
        root = Site.objects.get(is_default_site=True).root_page
        manager = ImportManager(root, fixture('image_fixture'))
        manager.add_importers([
            PagesImporter('apie', 'apie'),
        ])
        image_count = Image.objects.filter(filename='steigiamasis.jpg').count()
        self.assertEqual(image_count, 1)
