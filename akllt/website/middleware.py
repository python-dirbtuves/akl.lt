from django import http


class LegacyRedirectMiddleware(object):
    def process_response(self, request, response):
        if request.path == '/naujienos/' and 'id' in request.GET:
            return http.HttpResponsePermanentRedirect(
                '/naujienos/naujiena_%s' % request.GET['id']
            )
        else:
            return response
