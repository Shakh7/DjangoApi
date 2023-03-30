# todo/todo_api/urls.py : API urls.py
from django.urls import path

from .views import (
    UserListApiView,
)

urlpatterns = [
    path('users', UserListApiView.as_view()),
]
