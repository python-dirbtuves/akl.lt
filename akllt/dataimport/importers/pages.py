from akllt.pages.models import StandardPage

from akllt.dataimport.importers.base import BaseImporter


class PagesImporter(BaseImporter):
    page_class = StandardPage
