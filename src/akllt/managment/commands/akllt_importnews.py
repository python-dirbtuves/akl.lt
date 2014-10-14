from django.core.management.base import BaseCommand, CommandError

from polls.models import Poll


class Command(BaseCommand):
    args = '<directory name>'
    help = 'Imports data from old akl.lt website'

    def handle(self, *args, **options):
        news_count = 0

        self.stdout.write('Successfully imported %d news items' % news_count)
