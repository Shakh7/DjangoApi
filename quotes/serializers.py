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


class QuoteSerializer(serializers.ModelSerializer):
    car_make = serializers.CharField(source='car_make.name')
    car_model = serializers.CharField(source='car_model.name')
    pick_up_address = CitySerializer()
    drop_off_address = CitySerializer()
    customer = CustomerSerializer()

    class Meta:
        model = Quote
        fields = [
            'id', 'car_make', 'car_model', 'car_year', 'pick_up_address', 'drop_off_address', 'pick_up_date',
            'customer', 'created_at'
        ]
