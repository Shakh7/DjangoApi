from rest_framework import generics
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.user_type == 'admin' or request.user.user_type == 'super_admin'
        )


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
