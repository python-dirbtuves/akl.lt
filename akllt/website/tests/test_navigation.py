from django.test import TestCase

from wagtail.wagtailcore.models import Page

from akllt.website import navigation as nav
from akllt.dataimport.tests.utils import get_default_site


# pylint: disable=invalid-name
class NavigationTests(TestCase):
    def test_get_top_menu_page(self):
        get_default_site()

        def add_page(root, **kw):
            return root.add_child(instance=Page(live=True, **kw))

        root = Page.objects.get(url_path='/')

        p1 = add_page(root, title='p1', show_in_menus=True)
        p2 = add_page(p1, title='p2', show_in_menus=True)
        p3 = add_page(p2, title='p3', show_in_menus=False)
        p4 = add_page(p3, title='p4', show_in_menus=False)

        self.assertEqual(nav.get_top_menu_page(None), None)
        self.assertEqual(nav.get_top_menu_page(root), None)
        self.assertEqual(nav.get_top_menu_page(p1).title, 'p1')
        self.assertEqual(nav.get_top_menu_page(p2).title, 'p2')
        self.assertEqual(nav.get_top_menu_page(p3).title, 'p2')
        self.assertEqual(nav.get_top_menu_page(p4).title, 'p2')
