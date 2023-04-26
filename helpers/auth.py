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


class SessionAuthAPIListView(generics.ListAPIView):
    pass
