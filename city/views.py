from rest_framework import generics, permissions
from helpers.auth import IsAdmin
from .models import City
from .serializers import CitySerializer
import json
from rest_framework.authentication import BasicAuthentication


class CityListView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAdmin, permissions.IsAuthenticated]

    # authentication_classes = [BasicAuthentication]


class CitySearchView(generics.ListAPIView):
    serializer_class = CitySerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        query = self.kwargs['search']

        print(self.request.get_host())

        # with open('assets/us_states.json') as f:
        #     states = json.load(f)
        #     print(states)

        if query:
            queryset = City.search(query)
        else:
            queryset = City.objects.none()
        return queryset
