from rest_framework import viewsets
from .models import Vehicle, VehicleMake
from .serializers import VehicleSerializer, VehicleMakeSerializer
from .filters import VehicleFilter, MakeFilter
from .tasks import create_vehicle


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return VehicleFilter(self.request.GET, queryset=qs).qs


class VehicleMakeViewSet(viewsets.ModelViewSet):
    queryset = VehicleMake.objects.all().order_by('name')
    serializer_class = VehicleMakeSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return MakeFilter(self.request.GET, queryset=qs).qs


class VehicleModelViewSet(viewsets.ModelViewSet):
    queryset = VehicleMake.objects.all().order_by('name')
    serializer_class = VehicleMakeSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return MakeFilter(self.request.GET, queryset=qs).qs


class VehicleRegisterViewSet(viewsets.ModelViewSet):
    queryset = VehicleMake.objects.all().order_by('name')
    serializer_class = VehicleMakeSerializer

    def get(self):
        import os
        import json
        current_directory = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(current_directory, 'cars.json')

        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        for item in data["results"]:
            create_vehicle.delay(item)
