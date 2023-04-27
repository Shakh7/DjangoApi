from django.shortcuts import render

from users.models import CustomUser
from .serializers import LeadSerializer
from .models import Lead as Lead
# Create your views here.

from helpers.auth import SessionAuthAPIListView, IsAdmin


class LeadListApiView(SessionAuthAPIListView):
    permission_classes = [IsAdmin]
    serializer_class = LeadSerializer

    def get_queryset(self):
        user = CustomUser.objects.create(
            id=1,
            full_name='id 1 user',
            email='email1@gmail.comS'
        )
        user.save()

        return Lead.objects.all()
