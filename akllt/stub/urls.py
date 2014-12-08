from django.conf.urls import patterns, url


urlpatterns = patterns(
    'akllt.stub.views',
    url(r'^nuorodos', 'nuorodos', name='nuorodos'),
    url(r'^atviras_kodas', 'atviras_kodas', name='atviras_kodas'),
    url(r'^wiki', 'wiki', name='wiki'),
    url(r'^programos', 'programos', name='programos'),
)
