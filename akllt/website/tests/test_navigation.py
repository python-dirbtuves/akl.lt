from django.test import TestCase

from wagtail.wagtailcore.models import Page

from akllt.common import treeutils
from akllt.website import navigation as nav
from akllt.dataimport.tests.utils import get_default_site
from akllt.website.templatetags import navtags


def node(name, show_in_menus=True, live=True):
    return Page(
        slug=name, title=name,
        show_in_menus=show_in_menus,
        live=live,
    )


def strip(items):
    return [item.strip() for item in items]


# pylint: disable=invalid-name,unbalanced-tuple-unpacking
class NavigationTests(TestCase):
    def test_get_top_menu_page(self):
        home = get_default_site().root_page
        treeutils.create_tree(home, [
            node('p1'), [
                node('p2'), [
                    node('p3', show_in_menus=False), [
                        node('p4', show_in_menus=False),
                    ],
                ],
            ],
        ])
        p1, (p2, (p3, (p4,))) = treeutils.grow_tree(home.get_descendants())

        self.assertEqual(nav.get_top_menu_page(None), None)
        self.assertEqual(nav.get_top_menu_page(home), None)
        self.assertEqual(nav.get_top_menu_page(p1).title, 'p1')
        self.assertEqual(nav.get_top_menu_page(p2).title, 'p1')
        self.assertEqual(nav.get_top_menu_page(p3).title, 'p1')
        self.assertEqual(nav.get_top_menu_page(p4).title, 'p1')


class ManuTreeTests(TestCase):
    def test_menu_tree(self):
        home = get_default_site().root_page
        treeutils.create_tree(home, [
            node('p1'), [
                node('p2'),
                node('p3', show_in_menus=False),
                node('p4'), [
                    node('p5'),
                ],
            ],
            node('p6'),
        ])

        p4 = Page.objects.get(title='p4')
        menu = navtags.sidebar_menu({'self': p4})
        self.assertEqual(menu.splitlines(), strip([
            '<ul class="depth-1 nav nav-pills nav-stacked">',
            '  <li>',
            '    <a href="/p1/p2/">p2</a>',
            '  </li>',
            '  <li class="active">',
            '    <a href="#">p4</a>',
            '    <ul class="depth-2 nav nav-pills nav-stacked">',
            '      <li>',
            '        <a href="/p1/p4/p5/">p5</a>',
            '      </li>',
            '    </ul>',
            '  </li>',
            '</ul>',
        ]))
