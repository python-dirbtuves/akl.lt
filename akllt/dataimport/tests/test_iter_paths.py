import unittest

from akllt.dataimport.importers.base import BaseImporter
from akllt.dataimport.tests.utils import fixture


class IterPathsTests(unittest.TestCase):
    def assert_paths(self, path, expected):
        importer = BaseImporter(path.name.title(), path.name)
        importer.path = path
        paths = [
            str(p.path.relative_to(importer.path))
            for p in importer.iterate_paths()
        ]
        self.assertEqual(sorted(paths), expected)

    def test_image_fixture(self):
        self.assert_paths(fixture('image_fixture/apie'), ['apie.html'])
        self.assert_paths(fixture('image_fixture/naujienos'), [
            'naujiena_0007', 'naujiena_0944', 'naujiena_0985', 'naujiena_1020',
        ])
        self.assert_paths(fixture('image_fixture/skaitykla'), [
            'pranesimai.html',
        ])

    def test_whole_export(self):
        self.assert_paths(fixture('whole_export/ak'), [
            '1doc.gif',
            'atviri_standartai',
            'atviri_standartai.html',
            'atviri_standartai/atviri_standartai.zpt',
            'dokumentacija',
            'dokumentacija.html',
            'dokumentacija/jabber.html',
            'dokumentacija/vertimas.html',
            'floss.html',
            'free-sw.html',
            'knygos',
            'knygos.html',
            'knygos/AKrinkinys.png',
            'knygos/Grafine_aplinka_KDE3.png',
            'knygos/IT_11-12_1d.png',
            'knygos/KDE3_atmintine.png',
            'knygos/Linux_atmintine_1.png',
            'knygos/Linux_sistemos_administravimas.png',
            'knygos/MySQL4_vadovas.png',
            'knygos/OpenOffice.png',
            'knygos/OpenOffice_atmintine.png',
            'knygos/PHP4_vadovas.png',
            'knygos/cathedral_and_bazaar.png',
            'knygos/nuo-win-prie-lin.png',
            'knygos/nuo_win_prie_lin.html',
            'laisve.zpt',
            'licencijos',
            'licencijos/apie.html',
            'licencijos/copyleft.html',
            'licencijos/gpl.html',
            'licencijos/kategorijos.html',
            'licencijos/lgpl.html',
            'osd.html',
            'sekme.html',
        ])
        self.assert_paths(fixture('whole_export/naujienos'), [
            'naujiena_0001', 'naujiena_0044',
        ])
