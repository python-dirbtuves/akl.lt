from django.conf.urls import patterns, include, url
from django.conf import settings

from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailsearch.urls import frontend as wagtailsearch_frontend_urls

urlpatterns = patterns('',  # noqa
    url(r'^$', 'akllt.views.index', name='index'),
    url(r'^naujienos', 'akllt.views.naujienos', name='naujienos'),
    url(r'^nuorodos', 'akllt.views.nuorodos', name='nuorodos'),
    url(r'^atviras_kodas', 'akllt.views.atviras_kodas', name='atviras_kodas'),
    url(r'^wiki', 'akllt.views.wiki', name='wiki'),
    url(r'^programos', 'akllt.views.programos', name='programos'),
    url(r'^apie', 'akllt.views.apie', name='apie'),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^search/', include(wagtailsearch_frontend_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    url(r'', include(wagtail_urls)),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.conf.urls.static import static

    urlpatterns += (
        staticfiles_urlpatterns() +
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
