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
    id = serializers.CharField()
    car_make = serializers.CharField(source='car_make.name')
    car_model = serializers.CharField(source='car_model.name')
    car_year = serializers.IntegerField()

    pick_up_date = serializers.DateField()
    is_operable = serializers.BooleanField()

    customer = serializers.SerializerMethodField(method_name='get_customer')
    # client_names = serializers.SerializerMethodField(method_name='get_client_names')

    origin = serializers.SerializerMethodField(method_name='get_departure')
    destination = serializers.SerializerMethodField(method_name='get_destination')
    quote_clients = serializers.SerializerMethodField(method_name='get_quote_clients')

    created_at = serializers.DateTimeField()
    notes = serializers.CharField()

    def get_quote_clients(self, obj):
        clients = []
        for lead in obj.leads.all():
            clients.append({
                'client': {
                    'id': lead.client.id,
                    'full_name': lead.client.full_name,
                },
                'price': lead.price
            })
        return clients

    def get_customer(self, obj):
        return {
            'full_name': obj.customer.first_name + ' ' + obj.customer.last_name,
            'email': obj.customer.email
        }

    def get_destination(self, obj):
        return {
            'zip_code': obj.destination.zip_code,
            'city_name': obj.destination.city_name,
            'state_name': obj.destination.state_name,
            'state_code': obj.destination.state_code,
        }

    def get_departure(self, obj):
        return {
            'zip_code': obj.origin.zip_code,
            'city_name': obj.origin.city_name,
            'state_name': obj.origin.state_name,
            'state_code': obj.origin.state_code,
        }

    # def get_client_names(self, obj):
    #     clients = obj.clients.all()
    #     return [{'full_name': client.full_name, 'email': client.email} for client in clients]
