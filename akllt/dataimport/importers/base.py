import os
import lxml.html
import collections
import datetime
import functools
import pathlib

from wagtail.wagtailcore.models import Page

from akllt.dataimport.z2loader import load_metadata

ImportItem = collections.namedtuple('ImportItem', ['path', 'created', 'page'])
ImportItem.__new__ = functools.partial(
    ImportItem.__new__, created=None, page=None
)


class BaseImporter(object):
    """

    Whole importer workflow:

    1. __init__(page_title, page_slug) called from management command

    2. set_up(root_page, base_path) called from ImportManager.add_importers

    3. iterate_items() yields item, called from ImportManager.iterate

       1. iterate_paths() yields path

    4. item = import_(item) called from management command

        1. data = parse_metadata(item)

        2. parent = get_parent_page(item.path)

           3. page, created = create_page(parent, data)

              1. prepare_page_instance(page, data)

        3. page, created = create_page(parent, data)

           1. prepare_page_instance(page, data)

    """

    model_class = Page
    root_page_class = Page

    def __init__(self, page_title, page_slug):
        self.page_title = page_title
        self.page_slug = page_slug

    def set_up(self, root_page, base_path):
        self.path = self.get_path(base_path)
        self.root = self.get_root_page(root_page)

    def get_path(self, base_path):
        return base_path / self.page_slug

    def get_root_page(self, root):
        return root.add_child(instance=self.root_page_class(
            title=self.page_title,
            slug=self.page_slug,
        ))

    def get_parent_page(self, path):
        return self.root

    def iterate_paths(self):
        for base, dirnames, filenames in os.walk(str(self.path)):
            base = pathlib.Path(base)

            # Yield all files, that have entry in .z2meta.
            for filename in filenames:
                path = base / filename
                if (base/'.z2meta'/filename).exists():
                    yield path

            # Visit only directories containing .z2meta.
            dirnames[:] = [
                dirname for dirname in dirnames
                if (base/dirname/'.z2meta').exists()
            ]

            # Yield all directories containing .z2meta.
            for dirname in dirnames:
                yield base / dirname

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
        data['slug'] = item.path.stem if item.path.suffix else item.path.name
        data['date'] = self.parse_date(data.get('date'))
        return data

    def import_(self, item):
        data = self.parse_metadata(item)
        parent = self.get_parent_page(item.path)
        page, created = self.create_page(parent, data)
        return item._replace(created=created, page=page)

    def create_page(self, parent, data):
        try:
            instance = (
                self.page_class.objects.child_of(parent).get(slug=data['slug'])
            )
        except self.page_class.DoesNotExist:
            instance = self.page_class(slug=data['slug'])

        self.prepare_page_instance(instance, data)

        if instance.pk:
            created = False
            instance.save()
        else:
            created = True
            instance = parent.add_child(instance=instance)

        return instance, created

    def prepare_page_instance(self, instance, data):
        instance.title = data['title']
        instance.date = data['date']
        instance.body = data['body']

    def image_finder(self, path):
        images = lxml.html.parse(str(path)).xpath('//img/@src')
        base = path.parent
        return [(base/image).resolve() for image in images]
