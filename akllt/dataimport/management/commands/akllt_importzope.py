import tqdm

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.models import Site
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from akllt.homepage.models import IndexPage
from akllt.dataimport.importmanager import ImportManager
from akllt.dataimport.importers.news import NewsImporter
from akllt.dataimport.importers.pages import PagesImporter
from akllt.dataimport.convertlinks import convert_links


class Command(BaseCommand):
    args = '<directory name>'
    help = 'Imports data from old akl.lt website'

    # pylint: disable=too-many-locals
    def handle(self, export_dir, *args, **options):
        verbosity = int(options['verbosity'])

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@localhost', 'admin')

        root = Page.objects.get(url_path='/')
        if not Page.objects.filter(url_path='/akl/').exists():
            site_root = root.add_child(instance=IndexPage(
                title='AKL',
                slug='akl',
            ))
            site = Site.objects.get(is_default_site=True)
            site.root_page = site_root
            site.save()
        else:
            site_root = Page.objects.get(url_path='/akl/')

        manager = ImportManager(site_root, export_dir)
        manager.add_importers([
            NewsImporter('Naujienos', 'naujienos', in_menu=False),
            PagesImporter('Atviras kodas', 'ak', in_menu=True),
            PagesImporter('Apie AKL', 'apie', in_menu=True),
            PagesImporter('Projektai', 'projektai', in_menu=True),
            PagesImporter('Skaitykla', 'skaitykla', in_menu=True),
            PagesImporter('Rėmėjai', 'remejai', in_menu=True),
            PagesImporter('Nuorodos', 'nuorodos', in_menu=True),
            PagesImporter('Balsavimas', 'balsavimas', in_menu=False),
            PagesImporter('Programos', 'programos', in_menu=False),
            PagesImporter('2004', '2004', in_menu=False),
            PagesImporter('2005', '2005', in_menu=False),
            PagesImporter('2006', '2006', in_menu=False),
            PagesImporter('2009', '2009', in_menu=False),
            PagesImporter('2010', '2010', in_menu=False),
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
            total=(n_updated + n_created),
        ))

        pages = (p.specific for p in Page.objects.all())
        if verbosity == 1:
            total = Page.objects.count()
            generator = tqdm.tqdm(convert_links(pages), total=total)
        else:
            generator = convert_links(pages)

        total = sum(1 for _ in generator)

        self.stdout.write((
            'Successfully converted links in {total} pages.'
        ).format(total=total))
