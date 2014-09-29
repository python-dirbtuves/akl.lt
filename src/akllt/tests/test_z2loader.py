# coding: utf-8
from __future__ import unicode_literals 
import unittest
import pkg_resources
import pathlib

from akllt.z2loader import load_metadata


class Z2LoaderTests(unittest.TestCase):
    def test_z2loader(self):
        path = pkg_resources.resource_filename(
            'akllt', 'tests/fixtures/naujienos/.z2meta/naujiena_0001',
        )
        path = pathlib.Path(path)
        assert path.exists()

        meta = load_metadata(str(path))
        self.assertEqual(meta, {
            'date': '2002-10-15',
            'title': 'Konkursas',
            'blurb': '\n'.join([
                '<p>Vilniuje, dvi dienas vyko Infobalt organizuotas konkursas',
                '„Geriausias 2002 metų lietuviškas informacinių technologijų,',
                'telekomunikacijų ir elektronikos (ITTE) produktas. AKL konkursui',
                'pristatė atvirojo kodo programų rinkinį "Laisvų programų CD" Konkursui',
                'iš viso buvo pateikti 32 įvairūs sprendimai. Iš viso planuojama skirti',
                'septynias nominacijas. Konkurso rezultatai bus paskelbti parodos',
                '"Infobalt 2002" paskutinę dieną spalio 26d., šeštadienį, 15:00.',
            ])
        })
        self.assertIn('„Geriausias 2002 metų lietuviškas informacinių technologijų,', meta['blurb'])
