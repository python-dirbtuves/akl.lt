import collections

from django import template

from akllt.website import navigation as nav

register = template.Library()

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


@register.inclusion_tag('website/tags/sidebar_menu.html', takes_context=True)
def sidebar_menu(context):
    calling_page = context.get('self')
    top_menu_page = nav.get_top_menu_page(calling_page)
    if top_menu_page is not None:
        pages = top_menu_page.get_children().live().in_menu()
    else:
        pages = []

    menu = []
    for page in pages:
        menu.append(MenuItem(
            page=page,
            active=(calling_page and calling_page.url == page.url),
        ))

    return {
        'menu': menu,
        'request': context['request'],  # required by the pageurl tag
    }
