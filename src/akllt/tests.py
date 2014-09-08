from django.test.testcases import TransactionTestCase
from homophony import BrowserTestCase, Browser


class SmokeTest(TransactionTestCase):

    def test_nothing(self):
        self.client.get('/')


class FoobarTestCase(BrowserTestCase):

    def test_home(self):
        browser = Browser()
        browser.open('http://testserver')
        browser.getLink('Naujienos').click()
        self.assertEquals(browser.title, 'Atviras Kodas Lietuvai')
