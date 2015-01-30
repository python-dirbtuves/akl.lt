import django.template

import akllt.website.helpers.login as login_helper

from allauth.socialaccount.providers.openid.forms import LoginForm

register = django.template.Library()


@register.inclusion_tag('website/tags/login_page.html', takes_context=True)
def login_page(context):
    request = context['request']
    return {
        'auth_providers': login_helper.get_auth_providers(request),
        'form': LoginForm(),
    }
