# todo/todo_api/urls.py : API urls.py
from django.urls import path

from .views import (
    ApiKeyListView, ApiKeyDetailView, ApiKeyUpdateView
)

urlpatterns = [
    path('keys/', ApiKeyListView.as_view()),
    path('keys/<str:key>/', ApiKeyDetailView.as_view()),
    path('keys/update/<str:key>/', ApiKeyUpdateView.as_view()),
]
