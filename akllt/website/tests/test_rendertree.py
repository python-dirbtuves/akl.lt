import unittest
import collections

from django.test import TestCase

from wagtail.wagtailcore.models import Page

from akllt.dataimport.tests.utils import get_default_site


def create_tree(parent, children):
    last = parent
    for child in children:
        if isinstance(child, list):
            create_tree(last, child)
        else:
            parent.add_child(instance=child)
        last = child


def grow_tree(flat_tree):
    """Takes flat tree and grows tree composed of nested lists."""

    tree = []
    stack = [(tree, 0)]
    for node in flat_tree:
        children, numchild = stack[-1]
        children.append(node)

        if node.numchild > 0:
            children.append([])
            stack.append((children[-1], node.numchild))
        else:
            numchild = 0
            while numchild <= 1 and stack:
                children, numchild = stack.pop()
            stack.append((children, numchild - 1))

    return tree


class PagesTreeTests(TestCase):
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

        create_tree(root, tree)
        self.assertEqual([root, tree], grow_tree(Page.get_tree(root)))


class Node(collections.namedtuple('Node', ('slug', 'numchild'))):
    def __repr__(self):
        return self.slug


class TreeTests(unittest.TestCase):
    def test_tree(self):
        # tree                  | numchild | stack
        # -----------------------+----------+---------------
        # home                  |        3 | [3]
        # |                     |          |
        # +-- p1                |        0 | [2]
        # |                     |          |
        # +-- p2                |        2 | [2, 2]
        # |   |                 |          |
        # |   +-- p21           |        0 | [2, 1]
        # |   |                 |          |
        # |   +-- p22           |        1 | [2, 1, 1]
        # |       |             |          |
        # |       +-- p221      |        1 | [2, 1, 1, 1)]
        # |           |         |          |
        # |           +-- p2211 |        0 | [1]
        # |                     |          |
        # +-- p3                |        0 | []

        tree = [
            Node('home', 3),
            Node('p1', 0),
            Node('p2', 2),
            Node('p21', 0),
            Node('p22', 1),
            Node('p221', 1),
            Node('p2211', 0),
            Node('p3', 0),
        ]

        self.assertEqual(grow_tree(tree), [
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
        ])
