import os
import pathlib

from wagtail.wagtailcore.models import Page

from akllt.pages.models import StandardPage
from akllt.dataimport.importers.base import BaseImporter
from akllt.dataimport.z2loader import parse_list_file


class PagesImporter(BaseImporter):
    page_class = StandardPage
    root_page_class = StandardPage

    def get_root_page(self, root):
        return root.add_child(instance=self.root_page_class(
            title=self.page_title,
            slug=self.page_slug,
            show_in_menus=True,
        ))

    def iterate_paths(self):
        for base, dirnames, filenames in os.walk(str(self.path)):
            base = pathlib.Path(base)

            # Yield only files from list file
            list_file = base / 'list'
            if list_file.exists():
                for filename in parse_list_file(list_file):
                    files_exists = (
                        (base / filename).exists() and
                        (base / '.z2meta' / filename).exists()
                    )
                    if files_exists:
                        yield base / filename

            # Visit only directories containing .z2meta.
            dirnames[:] = [
                dirname for dirname in dirnames
                if (base / dirname / '.z2meta').exists()
            ]

    def create_parent_pages(self, parent_page, parts):
        for part in parts:
            parent_page = parent_page.add_child(instance=self.page_class(
                title=part,
                slug=part,
                show_in_menus=True,
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
                return self.create_parent_pages(parent_page, parts)
        return parent_page

    def prepare_page_instance(self, instance, data):
        super(PagesImporter, self).prepare_page_instance(instance, data)
        instance.show_in_menus = True
