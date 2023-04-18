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

    def get_queryset(self):
        with open('core/cars.json', 'r') as file:
            data = json.load(file)
            for car_dict in data:
                car_name = car_dict['name']
                car, created = Car.objects.get_or_create(name=car_name)
                for model_dict in car_dict['models']:
                    model_name = model_dict['name']
                    model_series = model_dict['series']
                    car_model, created = CarModel.objects.get_or_create(name=model_name, series=model_series)
                    car.models.add(car_model)

        return Car.objects.all()


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
