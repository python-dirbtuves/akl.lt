import os
import re
import lxml.html
import collections
import datetime
import functools
import pathlib
import html
import urllib.parse

from django.core.files import File
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.models import Image
from wagtail.wagtaildocs.models import Document

from akllt.dataimport.z2loader import load_metadata

IMG_TAG_RE = re.compile(r'<img\b[^>]*>')
A_TAG_RE = re.compile(r'<a\b[^>]*>')

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

    4. item = import_item(item) called from management command

        1. data = parse_metadata(item)

        2. parent = get_parent_page(item.path)

           3. page, created = create_page(parent, item, data)

              1. prepare_page_instance(page, item, data)

        3. page, created = create_page(parent, item, data)

           1. prepare_page_instance(page, item, data)

    """

    model_class = Page
    root_page_class = Page

    def __init__(self, page_title, page_slug):
        self.page_title = page_title
        self.page_slug = page_slug

    def set_up(self, root_page, base_path):
        self.base_path = base_path
        self.path = self.get_path(base_path)
        self.root = self.get_root_page(root_page)

    def get_path(self, base_path):
        return base_path / self.page_slug

    def get_root_page(self, root):
        try:
            return (
                self.root_page_class.objects.child_of(root).
                get(slug=self.page_slug)
            )
        except self.root_page_class.DoesNotExist:
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
        data['body'] = self.parse_content(item.path, body)
        data['slug'] = item.path.stem if item.path.suffix else item.path.name
        data['date'] = self.parse_date(data.get('date'))
        return data

    def convert_url_to_path(self, path, url):
        if not url:
            return
        if urllib.parse.urlparse(url).scheme:
            return

        absolute_url = pathlib.PurePath(*[
            p
            for p in pathlib.PurePath(url.lstrip('/')).parts
            if p not in ('.', '..')
        ])

        if (self.base_path / absolute_url).exists():
            return self.base_path / absolute_url
        elif (path.parent / url).exists():
            return path.parent / url
        else:
            return path / url

    def parse_images(self, path, content):
        def get_image_format(attrs):
            classes = attrs.get('class', '').split()
            if 'lphoto' in classes:
                return 'left'
            elif 'rphoto' in classes:
                return 'right'
            else:
                return 'fullwidth'

        def replace_image_tag(match):
            attrs = lxml.html.fromstring(match.group(0)).attrib
            asset_path = self.convert_url_to_path(path.parent, attrs.get('src'))

            if asset_path:
                with asset_path.open('rb') as f:
                    image = Image.objects.create(
                        title=attrs.get('alt', attrs.get('title', '')),
                        file=File(f, asset_path.name),
                        width=attrs.get('width', 0),
                        height=attrs.get('height', 0),
                    )

                return '<embed %s/>' % ' '.join([
                    '%s="%s"' % (k, html.escape(v, quote=True)) for k, v in (
                        ('alt', image.title),
                        ('embedtype', 'image'),
                        ('format', get_image_format(attrs)),
                        ('id', str(image.pk)),
                    )
                ])
            else:
                return match.group(0)

        return IMG_TAG_RE.sub(replace_image_tag, content)

    def parse_links(self, path, content):
        suffixes = ('avi', 'doc', 'jpg', 'odp', 'odt', 'pdf', 'png', 'sxi')

        def href_to_path(href):
            if href:
                suffix = pathlib.PurePath(href).suffix.lstrip('.').lower()
                if suffix in suffixes:
                    return self.convert_url_to_path(path.parent, href)

        def replace_link_tag(match):
            attrs = lxml.html.fromstring(match.group(0)).attrib
            asset_path = href_to_path(attrs.get('href'))
            if asset_path:
                title = attrs.get('alt', attrs.get('title', asset_path.name))
                with asset_path.open('rb') as f:
                    document = Document.objects.create(
                        title=title,
                        file=File(f, asset_path.name),
                    )

                return '<a %s>' % ' '.join([
                    '%s="%s"' % (k, html.escape(v, quote=True)) for k, v in (
                        ('id', str(document.pk)),
                        ('linktype', 'document'),
                    )
                ])
            else:
                return match.group(0)

        return A_TAG_RE.sub(replace_link_tag, content)

    def parse_content(self, path, content):
        content = self.parse_images(path, content)
        content = self.parse_links(path, content)
        return content

    def import_all_items(self):
        for item in self.iterate_items():
            self.import_item(item)

    def import_item(self, item):
        data = self.parse_metadata(item)
        parent = self.get_parent_page(item.path)
        page, created = self.create_page(parent, item, data)
        return item._replace(created=created, page=page)

    def create_page(self, parent, item, data):
        try:
            instance = (
                self.page_class.objects.child_of(parent).get(slug=data['slug'])
            )
        except self.page_class.DoesNotExist:
            instance = self.page_class(slug=data['slug'])

        self.prepare_page_instance(instance, item, data)

        if instance.pk:
            created = False
            instance.save()
        else:
            created = True
            instance = parent.add_child(instance=instance)

        return instance, created

    def prepare_page_instance(self, instance, item, data):
        instance.title = data['title']
        instance.date = data['date']
        instance.body = data['body']
