import json

from rest_framework import generics, permissions
from django.db.models import Q
from helpers.auth import IsAdmin
from .models import Car, CarModel
from .serializers import CarSerializer
import json


class CarListView(generics.ListAPIView):
    serializer_class = CarSerializer
    permission_classes = [IsAdmin, permissions.IsAuthenticated]
    queryset = Car.objects.all()


class CarSearchView(generics.ListAPIView):
    serializer_class = CarSerializer
    permission_classes = [IsAdmin, permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.kwargs['search']
        if query:
            return Car.objects.filter(Q(name__icontains=query) | Q(models__name__icontains=query)).prefetch_related(
                'models').distinct()
        else:
            return Car.objects.all()
