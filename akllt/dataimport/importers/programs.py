from akllt.news.models import ProgramIndex
from akllt.news.models import ProgramPage

from akllt.dataimport.importers.base import BaseImporter


class ProgramsImporter(BaseImporter):
    page_class = ProgramPage
    root_page_class = ProgramIndex

    def iterate_paths(self):
        for path in self.path.iterdir():
            if path.name.startswith('programa_'):
                yield path

    def prepare_page_instance(self, instance, data):
        super(NewsImporter, self).prepare_page_instance(instance, data)
        instance.blurb = data['blurb']
