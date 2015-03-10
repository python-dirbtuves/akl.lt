from django.test import TestCase
from django.core.management import call_command

from wagtail.wagtailcore.models import Page

from akllt.dataimport.tests.utils import fixture
from akllt.dataimport.tests.utils import get_default_site


class ImportZopeCommandTests(TestCase):
    def test_command(self):
        get_default_site()
        self.assertEqual(Page.objects.count(), 2)
        call_command('akllt_importzope', fixture('whole_export'), verbosity=0)
        self.assertEqual(Page.objects.count(), 26)
