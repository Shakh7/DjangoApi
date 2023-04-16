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

    customer = serializers.SerializerMethodField(method_name='get_customer')
    client_names = serializers.SerializerMethodField(method_name='get_client_names')

    destination = serializers.SerializerMethodField(method_name='get_destination')
    departure = serializers.SerializerMethodField(method_name='get_departure')

    def get_customer(self, obj):
        return {
            'full_name': obj.customer.first_name + ' ' + obj.customer.last_name,
            'email': obj.customer.email
        }

    def get_destination(self, obj):
        return {
            'zip_code': obj.drop_off_address.zip_code,
            'city_name': obj.drop_off_address.city_name,
            'state_name': obj.drop_off_address.state_name,
            'state_code': obj.drop_off_address.state_code,
        }

    def get_departure(self, obj):
        return {
            'zip_code': obj.pick_up_address.zip_code,
            'city_name': obj.pick_up_address.city_name,
            'state_name': obj.pick_up_address.state_name,
            'state_code': obj.pick_up_address.state_code,
        }

    def get_client_names(self, obj):
        clients = obj.clients.all()
        return [{'full_name': client.full_name, 'email': client.email} for client in clients]
