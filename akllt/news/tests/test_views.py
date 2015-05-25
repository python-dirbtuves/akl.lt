from django_webtest import WebTest
from django.contrib.auth.models import User

from wagtail.wagtailcore.models import Page

from akllt.dataimport.tests.utils import get_default_site


class LegacyRedirectTests(WebTest):
    def setUp(self):
        super().setUp()
        root_page = get_default_site().root_page
        self.root = root_page.add_child(instance=Page(slug='naujienos'))
        User.objects.create_user('user')
        User.objects.create_superuser('admin', 'admin@example.com', 'secret')

    def test_suggest_news_story(self):
        resp = self.app.get('/news/create/', user='user')
        resp.form['title'] = 'Story 42'
        resp.form['body'] = '42'
        resp = resp.form.submit()

        page = Page.objects.get(title='Story 42')
        self.assertEqual(page.slug, 'story-42')
        self.assertFalse(page.latest_revision_created_at is None)

        resp = self.app.get('/admin/pages/%d/' % self.root.pk, user='admin')
        self.assertEqual(resp.lxml.xpath('//td[contains(@class, "listing")]//h2/a//text()'), '')
