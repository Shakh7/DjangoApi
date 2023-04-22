from django.utils.deprecation import MiddlewareMixin

from DjangoApi import settings


class XFrameOptionsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['X-Frame-Options'] = settings.X_FRAME_OPTIONS
        return response
