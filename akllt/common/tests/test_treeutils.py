import unittest
import collections

from django.test import TestCase

from wagtail.wagtailcore.models import Page

from akllt.dataimport.tests.utils import get_default_site
from akllt.common import treeutils


def slug_getter(node):
    return node.slug


class Node(collections.namedtuple('Node', ('slug', 'numchild'))):
    """Fake treebeard.models.Node used for testing."""
    def __repr__(self):
        return self.slug

    def get_children_count(self):
        return self.numchild


class FixtureMixin(object):
    def setUp(self):  # pylint: disable=invalid-name
        self.fixtures = Fixtures()
        super(FixtureMixin, self).setUp()


class GrowTreeTests(FixtureMixin, unittest.TestCase):
    def test_grow_tree(self):
        tree = treeutils.grow_tree(self.fixtures.dfs_tree_of_nodes())
        self.assertEqual(tree, self.fixtures.tree_of_nodes())

    def test_grow_tree_callback(self):
        dfs_tree = self.fixtures.dfs_tree_of_nodes()
        tree = treeutils.grow_tree(dfs_tree, lambda node: node.slug)
        self.assertEqual(tree, self.fixtures.tree_of_slugs())

    def test_grow_tree_iter(self):
        dfs_tree = self.fixtures.dfs_tree_of_nodes()

        tree = []
        for children, node in treeutils.grow_tree_iter(tree, dfs_tree):
            children.append(node.slug)

        self.assertEqual(tree, self.fixtures.tree_of_slugs())

    def test_empty_list(self):
        tree = treeutils.grow_tree([], slug_getter)
        self.assertEqual(tree, [])

    def test_single_node(self):
        tree = treeutils.grow_tree([Node('p1', 0)], slug_getter)
        self.assertEqual(tree, ['p1'])


class CreateTreeTests(FixtureMixin, TestCase):
    def test_create_tree(self):
        root = get_default_site().root_page
        tree = self.fixtures.tree_of_pages()
        treeutils.create_tree(root, tree)
        self.assertEqual(treeutils.grow_tree(root.get_descendants()), tree)

    def test_endless_recursion(self):
        root = get_default_site().root_page

        # Create a tree with recursive loop.
        tree = [Page(slug='recursive')]
        tree.append(tree)

        # Try to create that tree.
        treeutils.create_tree(root, tree)

        # See the results (hopefully without falling into endless recursion).
        result = treeutils.grow_tree(root.get_descendants(), slug_getter)
        self.assertEqual(result, ['recursive'])


class Fixtures(object):
    def dfs_tree_of_nodes(self):
        """DFS tree fixture.

        All test cases are provided with this tree structure:

            +-----------------------+----------+--------------+
            | tree                  | numchild | stack states |
            +-----------------------+----------+--------------+
            | home                  |        3 | [3]          |
            | |                     |          |              |
            | +-- p1                |        0 | [2]          |
            | |                     |          |              |
            | +-- p2                |        2 | [2, 2]       |
            | |   |                 |          |              |
            | |   +-- p21           |        0 | [2, 1]       |
            | |   |                 |          |              |
            | |   +-- p22           |        1 | [2, 1, 1]    |
            | |       |             |          |              |
            | |       +-- p221      |        1 | [2, 1, 1, 1] |
            | |           |         |          |              |
            | |           +-- p2211 |        0 | [1]          |
            | |                     |          |              |
            | +-- p3                |        0 | []           |
            +-----------------------+----------+--------------+

        """
        return [
            Node('home', 3),
            Node('p1', 0),
            Node('p2', 2),
            Node('p21', 0),
            Node('p22', 1),
            Node('p221', 1),
            Node('p2211', 0),
            Node('p3', 0),
        ]

    def tree_of_pages(self):
        """Tree fixture with nested lists."""
        return [
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

    def tree_of_nodes(self):
        """Fixture with nestes lists of nodes."""
        return [
            Node('home', 3), [
                Node('p1', 0),
                Node('p2', 2), [
                    Node('p21', 0),
                    Node('p22', 1), [
                        Node('p221', 1), [
                            Node('p2211', 0),
                        ],
                    ],
                ],
                Node('p3', 0),
            ],
        ]

    def tree_of_slugs(self):
        """Fixture with nested lists containing only slugs."""
        return [
            'home', [
                'p1',
                'p2', [
                    'p21',
                    'p22', [
                        'p221', [
                            'p2211',
                        ],
                    ],
                ],
                'p3',
            ],
        ]
