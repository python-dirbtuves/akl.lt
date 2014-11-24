# coding: utf-8

import pkg_resources
import pathlib

from django_webtest import WebTest
from wagtail.wagtailcore.models import Page

from akllt.pages.models import StandardPage


def import_pages(directory):
    assert pathlib.Path(directory).exists()


class SmokeTest(WebTest):

    def test_nothing(self):
        self.app.get('/')


class FoobarTestCase(WebTest):

    def test_home(self):
        index = self.app.get('/')
        assert 'Atviras Kodas Lietuvai' in index.click('Naujienos')


class ImportTestCase(WebTest):

    def test_import(self):  # pylint: disable=no-self-use
        import_pages(pkg_resources.resource_filename(
            'akllt', 'dataimport/tests/fixtures/pages'
        ))
        index = self.app.get('/')
        index.click('Apie')

    def test_create_page(self):  # pylint: disable=no-self-use
        homepage = Page.objects.get(id=2)
        homepage.add_child(instance=StandardPage(
            title='Atviras kodas Lietuvai',
            intro='Atviras kodas Lietuvai',
            body='Turinys',
            slug='atviras-kodas-lietuvai',
            live=True))
        self.app.get('/atviras-kodas-lietuvai/')
