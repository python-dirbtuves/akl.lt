import collections

from django import template

from akllt.website import navigation as nav
from akllt.common import treeutils
from akllt.common import htmlutils

register = template.Library()  # pylint: disable=invalid-name

MenuItem = collections.namedtuple('MenuItem', 'page, active')


@register.inclusion_tag('website/tags/top_menu.html', takes_context=True)
def top_menu(context):
    pages = context['request'].site.root_page.get_children().live().in_menu()
    top_menu_page = nav.get_top_menu_page(context.get('self'))

    menu = []
    for page in pages:
        menu.append(MenuItem(
            page=page,
            active=(top_menu_page and top_menu_page.url == page.url),
        ))

    return {
        'menu': menu,
        'request': context['request'],  # required by the pageurl tag
    }


@register.simple_tag(takes_context=True)
def sidebar_menu(context):

    def traverse(tree, depth=1):
        ul = htmlutils.Tag('ul', classes={
            'nav', 'nav-pills', 'nav-stacked', 'depth-' + str(depth),
        })
        yield ul.start()
        for page, children in tree:
            is_active = page.pk == calling_page.pk

            li = htmlutils.Tag('li')
            li.toggle_class('active', is_active)

            yield li.start()

            if is_active:
                yield htmlutils.tag('a', page.title, href='#')
            else:
                yield htmlutils.tag('a', page.title, href=page.url)

            if children:
                yield from traverse(children, depth=depth + 1)

            yield li.end()
        yield ul.end()

    if 'self' in context:
        calling_page = context['self']
        top_menu_page = nav.get_top_menu_page(calling_page)
        if top_menu_page:
            descendants = top_menu_page.get_descendants().live().in_menu()
            tree = treeutils.grow_tree(descendants)
            return '\n'.join(traverse(treeutils.transform(tree)))
    return ''


@register.inclusion_tag('website/tags/breadcrumb.html', takes_context=True)
def breadcrumb(context):
    calling_page = context.get('self')
    if calling_page:
        root = calling_page.get_root()
        pages = calling_page.get_ancestors().exclude(pk=root.pk)
    else:
        pages = []
    return {'pages': pages, 'calling_page': calling_page}
