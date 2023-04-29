from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LeadSerializer, CreateLeadSerializer
from .models import Lead as Lead
from helpers.auth import SessionAuthAPIListView, IsAdmin
from users.models import CustomUser
from quotes.models import Quote


class LeadListApiView(SessionAuthAPIListView):
    permission_classes = [IsAdmin]
    serializer_class = LeadSerializer

    def get_queryset(self):
        queryset = Lead.objects \
            .select_related('client') \
            .prefetch_related('quote__customer').all()

        return queryset


from django.db import IntegrityError


class CreateLeadAPIView(APIView):
    permission_classes = [IsAdmin]
    serializer_class = CreateLeadSerializer

    def post(self, request, *args, **kwargs):
        errors = []

        for quote in request.data:
            serializer = self.serializer_class(data=quote)
            serializer.is_valid(raise_exception=True)
            lead_data = serializer.validated_data
            client = CustomUser.objects.get(id=lead_data['client_id'])
            quote = Quote.objects.get(id=lead_data['quote_id'])

            old_lead, new_lead = Lead.objects.get_or_create(client=client, quote=quote, price=lead_data['price'])
            errors.append(old_lead.quote_id)

        return Response(status=status.HTTP_201_CREATED)

        # if errors:
        #     return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response(status=status.HTTP_201_CREATED)
