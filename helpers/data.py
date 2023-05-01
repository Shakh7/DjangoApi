from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 30

    def get_limit(self, request):
        if 'limit' in request.query_params:
            return int(request.query_params['limit'])
        return self.default_limit

    def get_offset(self, request):
        if 'offset' in request.query_params:
            return int(request.query_params['offset'])
        return 0

    def get_paginated_response(self, data):
        return Response({
            'count': self.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
