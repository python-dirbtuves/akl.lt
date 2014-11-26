import sys

import tqdm

from django.core.management.base import BaseCommand

from wagtail.wagtailcore.models import Page

import akllt.dataimport.news as newsparser
from akllt.news.models import NewsIndex


class Command(BaseCommand):
    args = '<directory name>'
    help = 'Imports data from old akl.lt website'

    def handle(self, news_folder, *args, **options):
        verbosity = int(options['verbosity'])
        n_created = 0
        n_updated = 0

        try:
            root = Page.objects.get(url_path='/')
        except Page.DoesNotExist:
            self.stderr.write('Can\'t find Wagtail root page.')
            sys.exit(1)

        try:
            news_index = NewsIndex.objects.descendant_of(root).get()
        except NewsIndex.DoesNotExist:
            news_index = root.add_child(instance=NewsIndex(
                title='Naujienos',
                url_path='/naujienos',
            ))

        if verbosity == 1:
            files = tqdm.tqdm(list(newsparser.iter_news_files(news_folder)))
        else:
            files = newsparser.iter_news_files(news_folder)

        for path in files:
            if verbosity > 1:
                self.stdout.write(str(path))
            try:
                news_item = newsparser.parse_metadata(path)
                _, created = newsparser.import_news_item(news_index, news_item)
            except:
                self.stdout.write(
                    '\n\nError occured while importing %s news file.' % path
                )
                raise

            if created:
                n_created += 1
            else:
                n_updated += 1

        self.stdout.write((
            'Successfully imported {n_created} and updated {n_updated}  news '
            'items. Total {total} news items.\n'
        ).format(
            n_created=n_created, n_updated=n_updated,
            total=n_updated+n_created,
        ))
