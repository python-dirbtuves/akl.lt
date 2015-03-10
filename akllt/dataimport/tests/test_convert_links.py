import unittest

import lxml.html

from akllt.dataimport.importers.pages import PagesImporter
from akllt.dataimport.tests.utils import fixture
from akllt.dataimport.tests.utils import get_default_site
from akllt.pages.models import StandardPage


class ConvertLinksTests(unittest.TestCase):
    @unittest.skip('TODO')
    def test(self):
        root = get_default_site().root_page
        importer = PagesImporter('Atviras kodas', 'ak')
        importer.set_up(root, fixture('whole_export'))
        importer.import_all_items()
        importer.post_process()

        page = StandardPage.objects.get(url_path='/home/ak/knygos/')
        links = list(lxml.html.fromstring(page.body).xpath('//a/@href'))
        self.assertEqual(links[0], '/ak/knygos/nuo_win_prie_lin/')
        self.assertEqual(links, [
            '/ak/knygos/nuo_win_prie_lin/',
            '/ak/knygos/nuo_win_prie_lin/',
            '/ak/knygos/AKrinkinys/',
            '/ak/knygos/AKrinkinys/',
            '/ak/knygos/linuxatmintine/',
            '/ak/knygos/linuxatmintine/',
            '/ak/knygos/openoffice/',
            '/ak/knygos/openoffice/',
            '/ak/knygos/openoffice_atmintine/',
            '/ak/knygos/openoffice_atmintine/',
            '/ak/knygos/IT_vadovelis/',
            '/ak/knygos/IT_vadovelis/',
            '/ak/knygos/linux_sistemos_administravimas/',
            '/ak/knygos/linux_sistemos_administravimas/',
            '/ak/knygos/php4_vadovas/',
            '/ak/knygos/php4_vadovas/',
            '/ak/knygos/mysql4_vadovas/',
            '/ak/knygos/mysql4_vadovas/',
            '/ak/knygos/kde_atmintine/',
            '/ak/knygos/kde_atmintine/',
            'http://www.kde.org',
            '/ak/knygos/grafine_aplinka_kde/',
            '/ak/knygos/grafine_aplinka_kde/',
            '/ak/knygos/cathedral_and_bazaar/',
            '/ak/knygos/cathedral_and_bazaar/',
        ])
