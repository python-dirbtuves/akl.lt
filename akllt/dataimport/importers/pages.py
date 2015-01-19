import posixpath

from wagtail.wagtailcore.models import Page

from akllt.pages.models import StandardPage
from akllt.dataimport.importers.base import BaseImporter


class PagesImporter(BaseImporter):
    page_class = StandardPage

    def get_root_page(self, root):
        return root.add_child(instance=Page(
            title=self.page_title,
            slug=self.page_slug,
        ))

    def create_parent_page(self, parent_page, parts):
        for part in parts:
            parent_page = parent_page.add_child(instance=Page(
                title=part,
                slug=part,
            ))
        return parent_page

    def get_parent_page(self, path):
        relative_path = path.parent.relative_to(self.path)
        parent_page = self.root
        for i, part in enumerate(relative_path.parts):
            try:
                parent_page = parent_page.get_children().get(slug=part)
            except Page.DoesNotExist:
                parts = relative_path.parts[i:]
                return self.create_parent_page(parent_page, parts)
        return parent_page
