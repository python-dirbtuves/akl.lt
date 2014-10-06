import datetime
import pathlib

from akllt.dataimport.z2loader import load_metadata


def import_news(directory):
    """Reads news from given directory.

    Directory should cantain Zope export, like this one:

        https://github.com/mgedmin/akl.lt-zope-export
    """
    path = pathlib.Path(directory)
    assert path.exists()
    for item in path.iterdir():
        if item.name.startswith('naujiena_'):
            z2meta_filename = item.parent / '.z2meta' / item.name
            news_story = load_metadata(z2meta_filename)
            news_story['date'] = datetime.datetime.strptime(
                news_story['date'], '%Y-%m-%d'
            ).date()
            with item.open() as f:
                news_story['body'] = f.read()
            yield news_story
