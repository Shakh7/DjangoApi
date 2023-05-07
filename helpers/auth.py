from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import BasePermission
from django.contrib.sessions.models import Session
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from users.models import CustomUser as User
from rest_framework_simplejwt.authentication import JWTAuthentication

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
        # if not referer or not referer.startswith('https://app.shipperauto.com'):
        #     return HttpResponse('Access Denied', status=403)
        return self.get_response(request)


class SessionAuthAPIListView(generics.ListAPIView):
    pass


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Call the parent class authenticate method to get the validated token and user object
        user, jwt = super().authenticate(request)

        # Implement your custom authentication logic here
        if not user.is_active:
            raise AuthenticationFailed('User account is not active.')

        # Return the validated user object
        return user, jwt
