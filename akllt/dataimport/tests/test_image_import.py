import unittest
import pathlib

from django.test import TestCase

from wagtail.wagtailcore.models import Site
from wagtail.wagtailimages.models import Image

from akllt.dataimport.importmanager import ImportManager
from akllt.dataimport.importers.pages import PagesImporter
from akllt.dataimport.importers.news import NewsImporter
from akllt.dataimport.tests.utils import fixture
from akllt.dataimport.tests.utils import get_default_site


class ImportImageTests(TestCase):
    def test_import_page_image(self):
        root = get_default_site().root_page
        importer = PagesImporter('apie', 'apie')
        importer.set_up(root, fixture('image_fixture'))
        importer.import_all_items()
        self.assertTrue(Image.objects.filter(title__in=(
            'AKL Rumšiškėse',
            'AKL steigiamasis susirinkimas (II)',
        )).exists())

    def test_import_news_image(self):
        root = get_default_site().root_page
        importer = NewsImporter('Naujienos', 'naujienos')
        importer.set_up(root, fixture('image_fixture'))
        importer.import_all_items()
        self.assertTrue(Image.objects.filter(title__in=(
            'MS penguin',
            'Programuokime smagiai su Scratch',
        )).exists())

    def test_parse_images(self):
        root = get_default_site().root_page
        path = fixture('image_fixture/apie/apie.html')
        importer = PagesImporter('apie', 'apie')
        importer.set_up(root, fixture('image_fixture'))
        result = importer.parse_images(path, '\n'.join([
            '<img src="../images/akl.jpg" alt="AKL Rumšiškėse"',
            '     height="181" width="285" border="0"',
            '     class="lphoto"/>',
        ]))
        self.assertEqual(result, (
            '<embed alt="AKL Rumšiškėse"'
            ' embedtype="image" format="left" id="1"/>'
        ))
