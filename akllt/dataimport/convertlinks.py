import posixpath
import re
import urllib.parse
import lxml.html

from wagtail.wagtailcore.models import Page

A_TAG_RE = re.compile(r'<a\b[^>]*>')
AKL_URL_RE = re.compile(r'http://(www\.)?akl\.lt')

URL_FIX_MAP = {
    '/programos/?doc=pramoga.html': '/programos/pramogai/',
    '/programos/?doc=project.html': '/programos/projektavimui/',
    '/programos/?doc=web.html': '/programos/webserveriai/',
    '/programos/?doc=office.html': '/programos/biurui/',
    '/programos/?doc=graphic.html': '/programos/vaizdui/',
    '/projektai/?doc=cd.html': '/projektai/lpcd/cd/',
    '/projektai/?doc=witfor.html': '/projektai/parodos/witfor/',
    '/projektai/?doc=Infobalt2003.html': '/projektai/parodos/Infobalt2003/',
    '/projektai/?doc=Infobalt2005.html': '/projektai/parodos/Infobalt2005/',
    '/apie/visuotinis/visuotinis/?doc=visuotinis06.html': '/apie/visuotinis/visuotinis06/',
    '/apie/?doc=visuotinis05.html': '/apie/visuotinis/visuotinis05/',
    'knygos/?doc=grafine_aplinka_kde.html': '/ak/knygos/grafine_aplinka_kde/',
    '/apie/?doc=akl_istatai.html': '/apie/istatai/',
    '../../2005/visuotinis/?doc=visuotinis2005_protokolas.html': '/2005/visuotinis/visuotinis2005_protokolas/',
    '?doc=eVitamins.html': '/projektai/eVitamins/',
    '?doc=cd.html': '/projektai/lpcd/cd/',
    '?doc=seminarai.html': '/projektai/seminarai/',
    '?doc=diskusijos.html': '/projektai/diskusijos/',
    '../ak/?doc=gpl.html': '/ak/licencijos/gpl/',
    '../akl/licencijos/?doc=gpl.html': '/ak/licencijos/gpl/',
}


def clean_link(link):
    if link and ('doc=' in link or 'id=naujiena_' in link):
        link = AKL_URL_RE.sub('', link)
        link = link[8:] if link.startswith('/akl-new/') else link
        return link


def get_converted_url(page, link):
    url = urllib.parse.urlparse(link)
    query = urllib.parse.parse_qs(url.query)

    if 'id' in query:
        doc, = query.pop('id')
        doc = '{}_{:0>4}'.format(*doc.split('_'))
    elif 'doc' in query:
        doc, = query.pop('doc')
        doc = doc[:-5] if doc.endswith('.html') else doc
        doc = doc[:-4] if doc.endswith('.zpt') else doc

    if link.startswith('/'):
        path = posixpath.join(url.path, doc)
    else:
        path = posixpath.join(posixpath.dirname(page.url.rstrip('/')), url.path, doc)

    path += '/'

    # pylint: disable=protected-access
    return url._replace(
        query=urllib.parse.urlencode(query, doseq=True),
        path=path,
    ).geturl()


def get_url_path(url):
    # pylint: disable=protected-access
    url_path = urllib.parse.urlparse(url)._replace(fragment='').geturl()
    return '/akl%s' % url_path


def format_wagtail_tag(page, link):
    if link in URL_FIX_MAP:
        url = URL_FIX_MAP[link]
    else:
        url = get_converted_url(page, link)

    url_path = get_url_path(url)
    try:
        ref_page = Page.objects.get(url_path=url_path)
    except Page.DoesNotExist:
        print(url_path)
        raise

    return '<a linktype="page", id="%d">' % ref_page.pk


def convert_page_link(page):
    def replace_links(match):
        attrs = lxml.html.fromstring(match.group(0)).attrib
        link = clean_link(attrs.get('href'))
        if link:
            return format_wagtail_tag(page, link)
        else:
            return match.group(0)

    page.body = A_TAG_RE.sub(replace_links, page.body)
    page.save()


def convert_links(pages):
    for page in pages:
        if hasattr(page, 'body'):
            convert_page_link(page)
        yield page
