# coding: utf-8

import pkg_resources
import pathlib

from django.test.testcases import TransactionTestCase
from django.test import TestCase
from homophony import BrowserTestCase, Browser
from wagtail.wagtailcore.models import Page

from akllt.models import StandardPage


def import_pages(directory):
    assert pathlib.Path(directory).exists()


class SmokeTest(TransactionTestCase):

    def test_nothing(self):
        self.client.get('/')


class FoobarTestCase(BrowserTestCase):

    def test_home(self):
        browser = Browser()
        browser.open('http://testserver')
        browser.getLink('Naujienos').click()
        self.assertEquals(browser.title, 'Atviras Kodas Lietuvai')


class ImportTestCase(BrowserTestCase, TestCase):

    def test_import(self):  # pylint: disable=no-self-use
        import_pages(pkg_resources
                     .resource_filename('akllt', 'tests/fixtures/pages'))
        browser = Browser()
        browser.open('http://testserver')
        browser.getLink('Apie').click()
        # expected_content = pkg_resources.resource_string(
        #     'akllt', 'test_data/pages/apie.html')
        # self.assertTrue(expected_content in browser.contents)

    def test_create_page(self):  # pylint: disable=no-self-use
        homepage = Page.objects.get(id=2)
        homepage.add_child(instance=StandardPage(
            title='Atviras kodas Lietuvai',
            intro='Atviras kodas Lietuvai',
            body='Turinys',
            slug='atviras-kodas-lietuvai',
            live=True))
        Browser('http://testserver/atviras-kodas-lietuvai/')
