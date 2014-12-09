from akllt.news.models import NewsIndex
from akllt.news.models import NewsStory

from akllt.dataimport.importers.base import BaseImporter


class NewsImporter(BaseImporter):
    page_class = NewsStory
    root_page_class = NewsIndex

    def iterate_paths(self):
        for path in self.path.iterdir():
            if path.name.startswith('naujiena_'):
                yield path

    def prepare_instance(self, instance, data):
        super(NewsImporter, self).prepare_instance(instance, data)
        instance.blurb = data['blurb']
