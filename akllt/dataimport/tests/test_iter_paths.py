import unittest

from akllt.dataimport.importers.base import BaseImporter
from akllt.dataimport.tests.utils import fixture


class IterPathsTests(unittest.TestCase):
    def assertPaths(self, path, expected):
        importer = BaseImporter(path.name.title(), path.name)
        importer.path = path
        paths = [
            str(p.relative_to(importer.path))
            for p in importer.iterate_paths()
        ]
        self.assertEqual(paths, expected)

    def test_image_fixture(self):
        self.assertPaths(fixture('image_fixture/apie'), ['apie.html'])
        self.assertPaths(fixture('image_fixture/naujienos'), [
            'naujiena_0944', 'naujiena_1020', 'naujiena_0007',
        ])
        self.assertPaths(fixture('image_fixture/skaitykla'), [
            'pranesimai.html',
        ])

    def test_whole_export(self):
        self.assertPaths(fixture('whole_export/ak'), [
            'atviri_standartai.html',
            'knygos.html',
            'sekme.html',
            'floss.html',
            'osd.html',
            'laisve.zpt',
            'dokumentacija.html',
            '1doc.gif',
            'free-sw.html',
            'atviri_standartai',
            'licencijos',
            'atviri_standartai/atviri_standartai.zpt',
            'licencijos/copyleft.html',
            'licencijos/lgpl.html',
            'licencijos/gpl.html',
            'licencijos/apie.html',
            'licencijos/kategorijos.html',
        ])
        self.assertPaths(fixture('whole_export/naujienos'), [
            'naujiena_0001', 'naujiena_0044',
        ])
