import unittest

from akllt.common import htmlutils


class TagTests(unittest.TestCase):
    def test_tag(self):
        tag = htmlutils.Tag('a', href='http://www.example.com/')
        self.assertEqual(tag.start(), '<a href="http://www.example.com/">')

    def test_attrs(self):
        tag = htmlutils.Tag('div')
        self.assertEqual(tag.attrs(attr='"<"'), ' attr="&quot;&lt;&quot;"')

    def test_classes(self):
        tag = htmlutils.Tag('div')
        tag.classes.add('active')
        self.assertEqual(tag.attrs(), ' class="active"')
