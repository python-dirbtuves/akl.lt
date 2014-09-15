# coding: utf-8
import pkg_resources

from django.test.testcases import TransactionTestCase
from homophony import BrowserTestCase, Browser


def import_pages(directory):
    pass


class SmokeTest(TransactionTestCase):

    def test_nothing(self):
        self.client.get('/')


class FoobarTestCase(BrowserTestCase):

    def test_home(self):
        browser = Browser()
        browser.open('http://testserver')
        browser.getLink('Naujienos').click()
        self.assertEquals(browser.title, 'Atviras Kodas Lietuvai')


class ImportTestCase(BrowserTestCase):

    def test_import(self):
        import_pages(pkg_resources
                     .resource_filename('akllt', 'test_data/pages'))
        browser = Browser()
        browser.open('http://testserver')
        browser.getLink('Apie').click()
        # expected_content = pkg_resources.resource_string(
        #     'akllt', 'test_data/pages/apie.html')
        # self.assertTrue(expected_content in browser.contents)
