# todo/todo_api/urls.py : API urls.py
from django.urls import path

from .views import (
    UserListApiView, ClientListApiView, confirm_email
)

urlpatterns = [
    path('users/', UserListApiView.as_view()),
    path('clients/', ClientListApiView.as_view(), name='clients_list'),
    path('confirm-email/', confirm_email, name='clients_detail'),
]
