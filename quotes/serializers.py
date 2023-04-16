from rest_framework import serializers
from cars.models import Car, CarModel
from city.serializers import CitySerializer
from customers.models import Customer
from users.models import CustomUser
from .models import Quote as Quote


class CarMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = [
            'id', 'name'
        ]


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = [
            'id', 'name'
        ]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'first_name', 'last_name', 'email', 'phone'
        ]


class QuoteSerializer(serializers.Serializer):
    car_make = serializers.CharField(source='car_make.name')
    car_model = serializers.CharField(source='car_model.name')
    car_year = serializers.IntegerField()
    pick_up_address = serializers.CharField(source='pick_up_address.get_full_name')
    drop_off_address = serializers.CharField(source='drop_off_address.get_full_name')
    pick_up_date = serializers.DateField()
    is_operable = serializers.BooleanField()
    customer_name = serializers.CharField(source='customer.get_full_name')
    client_names = serializers.SerializerMethodField(method_name='get_client_names')

    def get_client_names(self, obj):
        return list(obj.clients.values_list('username', flat=True))
