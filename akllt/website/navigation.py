def get_top_menu_page(page):
    """Returns top menu Page instance or None."""
    if page is None:
        return None
    else:
        return page.get_ancestors(inclusive=True).live().in_menu().first()
