from django_webtest import WebTest


class LegacyRedirectTests(WebTest):
    def assertRedirects(self, resp, url):
        self.assertEqual(resp.location, 'http://localhost:80%s' % url)

    def test_news_redirect(self):
        resp = self.app.get('/naujienos/', 'id=naujiena_200', status=301)
        self.assertRedirects(resp, '/naujienos/naujiena_200/')

    def test_page_redirect(self):
        resp = self.app.get('/ak/', 'doc=osd.html', status=301)
        self.assertRedirects(resp, '/ak/osd/')
