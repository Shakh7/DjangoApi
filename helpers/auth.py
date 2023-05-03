from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import BasePermission
from django.contrib.sessions.models import Session
from users.models import CustomUser as User


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'admin'


class RefererMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        referer = request.META.get('HTTP_REFERER')
        if not referer or not referer.startswith('https://app.shipperauto.com'):
            return JsonResponse({'error': 'Access Denied'}, status=403)
        return self.get_response(request)


class SessionAuthAPIListView(generics.ListAPIView):
    pass
