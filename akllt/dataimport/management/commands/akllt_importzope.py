import sys

import tqdm

from django.core.management.base import BaseCommand

from akllt.dataimport.exceptions import ImporterError
from akllt.dataimport.importmanager import ImportManager
from akllt.dataimport.wagtail import get_root_page
from akllt.dataimport.importers.news import NewsImporter
from akllt.dataimport.importers.pages import PagesImporter


class Command(BaseCommand):
    args = '<directory name>'
    help = 'Imports data from old akl.lt website'

    def handle(self, export_dir, *args, **options):
        verbosity = int(options['verbosity'])
        try:
            root = get_root_page()
        except ImporterError as e:
            self.stderr.write(e)
            sys.exit(1)

        manager = ImportManager(root, export_dir)
        manager.add_importers([
            NewsImporter('Naujienos', 'naujienos'),
            PagesImporter('ak', 'Atviras kodas'),
            PagesImporter('apie', 'Apie AKL'),
            PagesImporter('projektai', 'Projektai'),
            PagesImporter('skaitykla', 'Skaitykla'),
            PagesImporter('remejai', 'Rėmėjai'),
            PagesImporter('nuorodos', 'Nuorodos'),
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
                item = importer.import_(item)
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
