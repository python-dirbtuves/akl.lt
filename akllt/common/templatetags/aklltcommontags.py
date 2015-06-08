from django import template
from django.utils.safestring import mark_safe

from akllt.common import formrenderer

register = template.Library()


@register.simple_tag(name='formrenderer', takes_context=True)
def formrenderer_filter(context, form):
    return mark_safe(formrenderer.render_fields(context['request'], form))
