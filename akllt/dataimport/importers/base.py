import os
import collections
import datetime
import functools
import pathlib
import posixpath

from wagtail.wagtailcore.models import Page

from akllt.dataimport.z2loader import load_metadata

ImportItem = collections.namedtuple('ImportItem', ['path', 'created', 'page'])
ImportItem.__new__ = functools.partial(
    ImportItem.__new__, created=None, page=None
)


class BaseImporter(object):
    model_class = Page
    root_page_class = Page

    def __init__(self, page_title, page_slug):
        self.page_title = page_title
        self.page_slug = page_slug

    def set_up(self, root_page, base_path):
        self.path = self.get_path(base_path)
        self.root = self.get_root_page(root_page)
        return self

    def get_path(self, base_path):
        return base_path / self.page_slug

    def get_page(self, root):
        descendants = self.root_page_class.objects.descendant_of(root)
        try:
            return descendants.get(url_path=url_path)
        except self.root_page_class.DoesNotExist:
            return root.add_child(instance=self.root_page_class(
                title=self.page_title,
                url_path=url_path,
            ))

    def get_root_page(self, root):
        return root

    def get_relative_url_path(self, path):
        relative_url_path = path.parent.relative_to(self.path).as_posix()
        return posixpath.join(self.root.url_path, relative_url_path)

    def get_parent_page(self, path):
        if self.path == path.parent:
            return self.root
        else:
            return self.get_page(self.get_parent_page(path.parent))

    def iterate_paths(self):
        for base, dirnames, filenames in os.walk(str(self.path)):
            base = pathlib.Path(base)

            # Visit only directories containing .z2meta.
            dirnames[:] = [
                dirname for dirname in dirnames
                if (base/dirname/'.z2meta').exists()
            ]

            # Yield all directories containing .z2meta.
            for dirname in dirnames:
                yield base / dirname

            # Yield all files, that have entry in .z2meta.
            for filename in filenames:
                path = base / filename
                if (base/'.z2meta'/filename).exists():
                    yield path

    def iterate_items(self):
        for path in self.iterate_paths():
            yield ImportItem(path=path)

    def parse_date(self, datestring):
        try:
            return datetime.datetime.strptime(datestring, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return None

    def parse_metadata(self, item):
        if item.path.is_dir():
            z2meta_filename = item.path / '.z2meta' / '__this__'
            body = ''
        else:
            z2meta_filename = item.path.parent / '.z2meta' / item.path.name
            with item.path.open() as f:
                body = f.read()

        data = load_metadata(z2meta_filename)
        data['body'] = body
        data['url'] = item.path.name
        data['date'] = self.parse_date(data.get('date'))
        return data

    def import_(self, item):
        data = self.parse_metadata(item)
        parent = self.get_parent_page(item.path)
        page, created = self.import_item(parent, data)
        return item._replace(created=created, page=page)

    def import_item(self, parent, data):
        try:
            instance = self.page_class.objects.get(slug=data['url'])
        except self.page_class.DoesNotExist:
            instance = self.page_class(slug=data['url'])

        self.prepare_instance(instance, data)

        if instance.pk:
            created = False
            instance.save()
        else:
            created = True
            instance = parent.add_child(instance=instance)

        return instance, created

    def prepare_instance(self, instance, data):
        instance.title = data['title']
        instance.date = data['date']
        instance.body = data['body']
