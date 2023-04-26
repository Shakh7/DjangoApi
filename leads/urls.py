from django.urls import path

from .views import (
    LeadListApiView
)

urlpatterns = [
    path('leads/', LeadListApiView.as_view()),
]
