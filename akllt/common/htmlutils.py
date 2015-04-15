import html


def join(sep):
    def func(value):
        return ' '.join(value)
    return func


class Tag(object):
    scheme = [
        ('class', 'classes', set, join(' ')),
        ('id', 'id', None, None),
        ('name', 'name', None, None),
        ('data-*', 'data', dict, None),
        ('src', 'src', None, None),
        ('for', 'for_', None, None),
        ('type', 'type', None, None),
        ('href', 'href', None, None),
        ('value', 'value', None, None),
        ('title', 'title', None, None),
        ('alt', 'alt', None, None),
        ('aria-*', 'aria', dict, None),
        ('role', 'role', None, None),
    ]

    def __init__(self, name, **kwargs):
        self._tag_name = name
        for attr, prop, default, func in self.scheme:
            default = default() if default else None
            setattr(self, prop, kwargs.get(prop, default))

    def attrs(self, **kwargs):
        """Format html tag attrubutes in a specific order [1].

        [1] http://codeguide.co/#html-attribute-order

        """
        attrs = []

        for attr, prop, default, func in self.scheme:
            if attr.endswith('*'):
                attr = attr[:-1]
                value = kwargs.pop(prop, {})
                value.update(getattr(self, prop))
                if value:
                    for key, value in sorted(value.items()):
                        attrs.append((attr + key, value))
            else:
                value = kwargs.pop(prop, getattr(self, prop))
                if value:
                    value = func(value) if func else value
                    attrs.append((attr, value))

        for attr, value in sorted(kwargs.items()):
            if value:
                attrs.append((attr, value))

        for i, (key, value) in enumerate(attrs):
            attrs[i] = '{}="{}"'.format(key, html.escape(value, quote=True))

        if attrs:
            return ' ' + ' '.join(attrs)
        else:
            return ''

    def start(self):
        return '<{name}{attrs}>'.format(name=self._tag_name, attrs=self.attrs())

    def end(self):
        return '</{name}>'.format(name=self._tag_name)
