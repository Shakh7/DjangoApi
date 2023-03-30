from rest_framework import generics, permissions
from helpers.auth import IsAdmin
from .models import City
from .serializers import CitySerializer
from django.db.models import Q


class CityListView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAdmin, permissions.IsAuthenticated]


class CitySearchView(generics.ListAPIView):
    serializer_class = CitySerializer
    permission_classes = [IsAdmin, permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.kwargs['search']
        if query:
            queryset = City.search(query)
        else:
            queryset = City.objects.none()
        return queryset
