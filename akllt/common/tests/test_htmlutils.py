import unittest

from akllt.common import htmlutils


class TagTests(unittest.TestCase):
    def test_tag(self):
        tag = htmlutils.Tag('a', href='http://www.example.com/')
        self.assertEqual(tag.start(), '<a href="http://www.example.com/">')
        self.assertEqual(tag.end(), '</a>')

    def test_attrs(self):
        tag = htmlutils.Tag('div')
        self.assertEqual(tag.attrs(attr='"<"'), ' attr="&quot;&lt;&quot;"')

    def test_classes(self):
        tag = htmlutils.Tag('div')
        tag.classes.add('active')
        tag.classes.add('more')
        self.assertEqual(tag.attrs(), ' class="active more"')

    def test_data(self):
        tag = htmlutils.Tag('div')
        tag.data['item'] = '1'
        self.assertEqual(tag.attrs(), ' data-item="1"')

    def test_no_attrs(self):
        tag = htmlutils.Tag('div')
        self.assertEqual(tag.start(), '<div>')

    def test_toggle_class(self):
        tag = htmlutils.Tag('div')

        tag.toggle_class('active')
        self.assertEqual(tag.attrs(), ' class="active"')

        tag.toggle_class('active')
        self.assertEqual(tag.attrs(), '')

        tag.toggle_class('active', False)
        self.assertEqual(tag.attrs(), '')

        tag.toggle_class('active', True)
        tag.toggle_class('more')
        self.assertEqual(tag.attrs(), ' class="active more"')

        tag.toggle_class('active', False)
        self.assertEqual(tag.attrs(), ' class="more"')

    def test_tag_helper(self):
        tag = htmlutils.tag('a', 'link', href='#')
        self.assertEqual(tag, '<a href="#">link</a>')
