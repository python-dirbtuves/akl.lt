from django import http


class LegacyRedirectMiddleware(object):
    def process_request(self, request):
        """Redirect legacy links to new ones

        Currently this middleware handles these types of legacy links:

        - /ak/?doc=osd.html -> /ak/osd/

        - /naujienos/?id=naujiena_1047 -> /naujienos/naujiena_1047/

        """
        if request.path == '/naujienos/' and 'id' in request.GET:
            url = '/naujienos/%s/' % request.GET['id']
        elif 'doc' in request.GET:
            doc = request.GET['doc']
            tail = doc[:-5] if doc.endswith('.html') else doc
            url = '%s%s/' % (request.path, tail)
        else:
            url = None
        return url and http.HttpResponsePermanentRedirect(url)
