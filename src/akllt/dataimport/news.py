import datetime
import pathlib

from akllt.dataimport.z2loader import load_metadata


def parse_date(datestring):
    try:
        return datetime.datetime.strptime(datestring, '%Y-%m-%d').date()
    except ValueError:
        return None


def import_news(directory):
    """Reads news from given directory.

    Directory should contain Zope export, like this one:

        https://github.com/mgedmin/akl.lt-zope-export
    """
    path = pathlib.Path(directory)
    assert path.exists()
    for item in path.iterdir():
        if item.name.startswith('naujiena_'):
            z2meta_filename = item.parent / '.z2meta' / item.name
            news_story = load_metadata(z2meta_filename)
            news_story['date'] = parse_date(news_story.get('date'))
            with item.open() as f:
                news_story['body'] = f.read()
            news_story['url'] = item.name
            yield news_story
