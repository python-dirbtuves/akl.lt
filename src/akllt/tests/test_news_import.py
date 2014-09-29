import pathlib
import unittest

import pkg_resources

from akllt.z2loader import load_metadata


def iter_news(directory):
    path = pathlib.Path(directory)
    assert path.exists()
    for item in path.iterdir():
        if item.name.startswith('naujiena_'):
            z2meta_filename = item.parent / '.z2meta' / item.name
            news_item = load_metadata(z2meta_filename)
            with item.open() as f:
                news_item['body'] = f.read()
            yield news_item


def shorten_values(item):
    shortened = {}
    for key, value in item.items():
        if len(value) > 24:
            shortened[key] = '%s...' % value[:24]
        else:
            shortened[key] = value
    return shortened


class NewsImportTests(unittest.TestCase):
    def test_iter_news(self):
        news_folder = pkg_resources.resource_filename(
            'akllt', 'tests/fixtures/naujienos'
        )
        news = iter_news(news_folder)
        self.assertEqual(list(map(shorten_values, news)), [
            {
                'date': '2002-10-15',
                'title': 'Konkursas',
                'blurb': '<p>Vilniuje, dvi dienas ...',
                'body': '<p>Vilniuje, dvi dienas ...',
            },
        ])
