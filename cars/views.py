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
        query = self.kwargs['search']
        if query:
            return Car.objects.filter(
                Q(name__icontains=query.strip()) |
                Q(models__name__icontains=query.strip())
            ).prefetch_related('models').distinct()
        else:
            return Car.objects.all()
