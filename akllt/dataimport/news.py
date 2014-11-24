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
    path = pathlib.Path(directory)
    assert path.exists()
    for item in path.iterdir():
        if item.name.startswith('naujiena_'):
            yield item


def import_news_item(root, news_item):
    try:
        instance = NewsStory.objects.get(slug=news_item['url'])
    except NewsStory.DoesNotExist:
        instance = NewsStory(slug=news_item['url'])

    instance.title = news_item['title']
    instance.date = news_item['date']
    instance.blurb = news_item['blurb']
    instance.body = news_item['body']

    if instance.pk:
        created = False
        instance.save()
    else:
        created = True
        instance = root.add_child(instance=instance)

    return instance, created
