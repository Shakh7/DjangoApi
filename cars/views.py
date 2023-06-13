from django.db.models import Q
from helpers.auth import IsAuthenticated
from .models import Car, CarModel
from .serializers import CarSerializer
from helpers.auth import SessionAuthAPIListView
from rest_framework.permissions import AllowAny


class CarListView(SessionAuthAPIListView):
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]
    queryset = Car.objects.all()


class CarSearchView(SessionAuthAPIListView):
    serializer_class = CarSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        search_query = self.kwargs['search']
        if search_query:
            queries = search_query.split()  # Split search query into individual words
            query = Q()
            for keyword in queries:
                query &= (
                        Q(name__icontains=keyword.strip()) |
                        Q(models__name__icontains=keyword.strip())
                )

            return Car.objects.filter(query).prefetch_related('models').distinct()
        else:
            return Car.objects.all()
