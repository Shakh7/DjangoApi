from django.http import HttpResponseForbidden


class DomainRestrictionMiddleware:
    ALLOWED_DOMAINS = ['dashboard.shipperauto.com', 'shipperauto.com', 'api.shipperauto.com', '127.0.0.1:8000']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.get_host() not in self.ALLOWED_DOMAINS:
            return HttpResponseForbidden('Access denied')
        return self.get_response(request)
