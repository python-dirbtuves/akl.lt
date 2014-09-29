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
            'blurb': meta['blurb'],
        })
        self.assertIn('konkursas\n„Geriausias 2002 metų', meta['blurb'])
