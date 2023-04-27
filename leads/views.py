from django.shortcuts import render
from .serializers import LeadSerializer
from .models import Lead as Lead
# Create your views here.

from helpers.auth import SessionAuthAPIListView, IsAdmin


class LeadListApiView(SessionAuthAPIListView):
    permission_classes = [IsAdmin]
    serializer_class = LeadSerializer
    queryset = Lead.objects.all()
