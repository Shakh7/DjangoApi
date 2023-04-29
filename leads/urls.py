from django.urls import path

from .views import (
    LeadListApiView, CreateLeadAPIView
)

urlpatterns = [
    path('leads/', LeadListApiView.as_view(), name='lead_list'),
    path('leads/create/', CreateLeadAPIView.as_view(), name='lead_create')
]
