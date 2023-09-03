from .models import Vehicle, VehicleMake
import django_filters


class VehicleFilter(django_filters.FilterSet):
    year = django_filters.CharFilter(field_name='year', lookup_expr='exact')
    make = django_filters.CharFilter(field_name='make__name', lookup_expr='icontains')
    model = django_filters.CharFilter(field_name='model', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category', lookup_expr='icontains')

    class Meta:
        model = Vehicle
        fields = ['year', 'make', 'model', 'category']


class MakeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Vehicle
        fields = ['name']
