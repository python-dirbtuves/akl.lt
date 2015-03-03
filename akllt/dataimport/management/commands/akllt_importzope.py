import tqdm

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.models import Site
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from akllt.homepage.models import IndexPage
from akllt.dataimport.importmanager import ImportManager
from akllt.dataimport.importers.news import NewsImporter
from akllt.dataimport.importers.pages import PagesImporter


class Command(BaseCommand):
    args = '<directory name>'
    help = 'Imports data from old akl.lt website'

    def handle(self, export_dir, *args, **options):
        verbosity = int(options['verbosity'])

        User.objects.create_superuser('admin', 'admin@localhost', 'admin')

        root = Page.objects.get(url_path='/')
        site_root = root.add_child(instance=IndexPage(
            title='AKL',
            slug='akl',
        ))

        site = Site.objects.get(is_default_site=True)
        site.root_page = site_root
        site.save()

        manager = ImportManager(site_root, export_dir)
        manager.add_importers([
            NewsImporter('Naujienos', 'naujienos'),
            PagesImporter('Atviras kodas', 'ak'),
            PagesImporter('Apie AKL', 'apie', ),
            PagesImporter('Projektai', 'projektai'),
            PagesImporter('Skaitykla', 'skaitykla'),
            PagesImporter('Rėmėjai', 'remejai'),
            PagesImporter('Nuorodos', 'nuorodos'),
        ])

        if verbosity == 1:
            items = tqdm.tqdm(manager.iterate(), total=manager.get_total())
        else:
            items = manager.iterate()

        n_created = 0
        n_updated = 0

        for importer, item in items:
            if verbosity > 1:
                self.stdout.write(str(item.path))
            try:
                item = importer.import_item(item)
            except:
                self.stdout.write((
                    '\n\nError occured while importing {path} news file.'
                ).format(path=item.path))
                raise

            if item.created:
                n_created += 1
            else:
                n_updated += 1

        self.stdout.write((
            'Successfully imported {n_created} and updated {n_updated} '
            'items. Total {total} items processed.\n'
        ).format(
            n_created=n_created, n_updated=n_updated,
            total=n_updated+n_created,
        ))
