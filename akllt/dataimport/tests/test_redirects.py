from django_webtest import WebTest
from wagtail.wagtailcore.models import Site
from wagtail.wagtailredirects.models import Redirect

from akllt.news.models import NewsIndex
from akllt.news.models import NewsStory


class RedirectTests(WebTest):
    def test_redirect(self):
        """Test news redirect"""
        site = Site.objects.get(is_default_site=True)
        news_index = site.root_page.add_child(instance=NewsIndex(
            title='Naujienos',
            slug='naujienos',
        ))
        new_page = news_index.add_child(instance=NewsStory(
            title='Naujiena 200',
            slug='naujiena_200',
        ))
        Redirect.objects.create(
            old_path='/naujienos/?id=200',
            site=site,
            is_permanent=True,
            redirect_page=new_page,
        )

        # Open naujienos/?id=200
        page = self.app.get('/naujienos/', 'id=200', status=301)
        self.assertEqual(
            page.location, 'http://localhost:80/naujienos/naujiena_200'
        )
