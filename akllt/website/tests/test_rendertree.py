from django.test import TestCase

from wagtail.wagtailcore.models import Page

from akllt.dataimport.tests.utils import get_default_site


def build_tree(parent, children):
    last = parent
    for child in children:
        if isinstance(child, list):
            build_tree(last, child)
        else:
            parent.add_child(instance=child)
        last = child


def tree_to_nested_lists(parent):
    """
    root, [home, p1, [p2, [p3, [p4], p21]], p5]
    """
    tree = []
    stack = [(tree, 0)]
    for page in Page.get_tree(parent):
        node, numchild = stack[-1]
        node.append(page)

        if page.numchild > 0:
            children = []
            node.append(children)
            stack.append((children, page.numchild - 1))
        else:
            numchild = 0
            while numchild == 0 and stack:
                node, numchild = stack.pop()
            stack.append((node, numchild - 1))

    return tree


class NavigationTests(TestCase):
    def test_build(self):
        root = get_default_site().root_page

        tree = [
            Page(slug='p1'),
            Page(slug='p2'), [
                Page(slug='p21'),
                Page(slug='p22'), [
                    Page(slug='p221'), [
                        Page(slug='p2211'),
                    ]
                ]
            ],
            Page(slug='p3'),
        ]

        build_tree(root, tree)
        self.assertEqual([root, tree], tree_to_nested_lists(root))
