import datetime
import pathlib

from akllt.dataimport.z2loader import load_metadata
from akllt.news.models import NewsStory


def parse_date(datestring):
    try:
        return datetime.datetime.strptime(datestring, '%Y-%m-%d').date()
    except ValueError:
        return None


def parse_metadata(path):
    z2meta_filename = path.parent / '.z2meta' / path.name
    news_story = load_metadata(z2meta_filename)
    news_story['date'] = parse_date(news_story.get('date'))
    with path.open() as f:
        news_story['body'] = f.read()
    news_story['url'] = path.name
    return news_story


def iter_news_files(directory):
    """Reads news from given directory.

    Directory should contain Zope export, like this one:

        https://github.com/mgedmin/akl.lt-zope-export
    """
    path = pathlib.Path(directory)
    assert path.exists()
    for item in path.iterdir():
        if item.name.startswith('naujiena_'):
            yield item


def import_news_item(root, news_item):
    root.add_child(instance=NewsStory(
        title=news_item['title'],
        date=news_item['date'],
        blurb=news_item['blurb'],
        body=news_item['body'],
    ))
