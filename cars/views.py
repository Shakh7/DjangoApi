from django.db.models import Q
from helpers.auth import IsAdmin
from .models import Car, CarModel
from .serializers import CarSerializer
from helpers.auth import JWTAuthAPIListView


class CarListView(JWTAuthAPIListView):
    serializer_class = CarSerializer
    permission_classes = [IsAdmin]
    queryset = Car.objects.all()


class CarSearchView(JWTAuthAPIListView):
    serializer_class = CarSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        query = self.kwargs['search']
        if query:
            return Car.objects.filter(Q(name__icontains=query) | Q(models__name__icontains=query)).prefetch_related(
                'models').distinct()
        else:
            return Car.objects.all()
