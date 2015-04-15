import collections

from django import template
from wagtail.wagtailcore.models import Page

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
    calling_page = context.get('self')
    top_menu_page = Page.objects.get(slug='akl')

    lines = []

    def traverse(tree):
        lines.append('<ul>')
        for page, children in tree:
            tag = htmlutils.Tag('li')
            if page.url == calling_page.url:
                tag.classes.add('active')

            if children:
                lines.extend([
                    tag.start(),
                    page.title,
                    traverse(children),
                    tag.end(),
                ])
            else:
                lines.extend([
                    tag.start(),
                    page.title,
                    tag.end(),
                ])
        lines.append('</ul>')

    tree = treeutils.grow_tree(top_menu_page.get_ancestors())
    traverse(treeutils.transform(tree))

    return '\n'.join(lines)


@register.inclusion_tag('website/tags/breadcrumb.html', takes_context=True)
def breadcrumb(context):
    calling_page = context.get('self')
    if calling_page:
        root = calling_page.get_root()
        pages = calling_page.get_ancestors().exclude(pk=root.pk)
    else:
        pages = []
    return {'pages': pages, 'calling_page': calling_page}
