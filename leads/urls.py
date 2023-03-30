# todo/todo_api/urls.py : API urls.py
from django.urls import path

from .views import (
    LeadListApiView, LeadCreateView
)

urlpatterns = [
    path('leads/', LeadListApiView.as_view()),
    path('leads/create/', LeadCreateView.as_view()),
]
