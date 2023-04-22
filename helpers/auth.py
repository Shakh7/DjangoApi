from rest_framework.permissions import BasePermission
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class JWTAuthAPIListView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
