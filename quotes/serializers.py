from rest_framework import serializers


class QuoteSerializer(serializers.Serializer):
    id = serializers.CharField()

    car_make = serializers.CharField(source='car_make.name')
    car_model = serializers.CharField(source='car_model.name')
    car_year = serializers.IntegerField()

    origin = serializers.SerializerMethodField(method_name='get_departure')
    destination = serializers.SerializerMethodField(method_name='get_destination')

    quote_clients = serializers.SerializerMethodField(method_name='get_quote_clients')

    created_at = serializers.DateTimeField()
    is_operable = serializers.BooleanField()

    notes = serializers.CharField()

    shipper = serializers.IntegerField(source='shipper.id')

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
