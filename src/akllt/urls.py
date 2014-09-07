from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'akllt.views.index', name='index'),
    url(r'^naujienos', 'akllt.views.naujienos', name='naujienos'),
    url(r'^nuorodos', 'akllt.views.nuorodos', name='nuorodos'),
    url(r'^atviras_kodas', 'akllt.views.atviras_kodas', name='atviras_kodas'),
    url(r'^wiki', 'akllt.views.wiki', name='wiki'),
    url(r'^programos', 'akllt.views.programos', name='programos'),
    url(r'^apie', 'akllt.views.apie', name='apie'),
 
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

