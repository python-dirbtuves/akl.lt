import re
import unittest
import pathlib

from django.test import TestCase

from wagtail.wagtailcore.models import Site
from wagtail.wagtaildocs.models import Document

from akllt.dataimport.importmanager import ImportManager
from akllt.dataimport.importers.pages import PagesImporter
from akllt.dataimport.importers.news import NewsImporter
from akllt.dataimport.tests.utils import fixture
from akllt.dataimport.tests.utils import get_default_site
from akllt.pages.models import StandardPage


class ImportDocumentsTests(TestCase):
    def test_document_import(self):
        root = get_default_site().root_page
        importer = PagesImporter('Skaitykla', 'skaitykla')
        importer.set_up(root, fixture('image_fixture'))
        importer.import_all_items()

        # Check if Document instances are created.
        self.assertTrue(Document.objects.filter(title__in=(
            'Kazarinas-Technologijos-ir-etika.odt',
            '2007-03-17-Kazarinas-Laisvosios-programos-mokyme.odt',
            '2004-06-02_Seimas_atviri_standartai.pdf',
            'AKP_naudojimo_patirtis_AM.pdf',
        )).exists())

        # Check if HTML is replaced as intended.
        docid = lambda title: Document.objects.get(title=title).pk
        docids = [
            docid('Kazarinas-Technologijos-ir-etika.odt'),
            docid('2007-03-17-Kazarinas-Laisvosios-programos-mokyme.odt'),
            docid('2004-06-02_Seimas_atviri_standartai.pdf'),
            docid('AKP_naudojimo_patirtis_AM.pdf'),
        ]
        page = StandardPage.objects.get(url_path='/home/skaitykla/pranesimai/')
        self.assertEqual(re.findall(r'<a\b[^>]+>', page.body), [
            '<a href="http://www.vac.lt/seminaras/">',
            '<a href="http://www.mruni.lt/">',
            '<a id="%d" linktype="document">' % docids[0],
            '<a href="http://discovery.ot.lt/linma/">',
            '<a id="%d" linktype="document">' % docids[1],
            '<a href="http://www.lrs.lt/">',
            '<a href="http://www.lrs.lt/ivpk">',
            '<a href="http://www3.lrs.lt/pls/inter/ivpk_print.doc_view?key=234334">',
            '<a id="%d" linktype="document">' % docids[2],
            '<a id="%d" linktype="document">' % docids[3],
        ])
