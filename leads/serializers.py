from rest_framework import serializers
from .models import Lead
from quotes.models import Quote
from users.models import CustomUser


class LeadSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    client = serializers.SerializerMethodField(method_name='get_client')
    quote = serializers.SerializerMethodField(method_name='get_quote')
    created_at = serializers.DateTimeField()
    price = serializers.FloatField()

    def get_client(self, obj):
        return {
            'id': obj.client.id,
            'full_name': obj.client.full_name,
            'email': obj.client.email
        }

    def get_quote(self, obj):
        return {
            'id': obj.quote.id,
            'created_at': obj.quote.created_at
        }


class CreateLeadSerializer(serializers.Serializer):
    client_id = serializers.IntegerField()
    quote_id = serializers.CharField()
    price = serializers.FloatField()

    def validate(self, data):
        # Ensure that the client ID and quote ID correspond to valid objects
        try:
            client = CustomUser.objects.get(id=data['client_id'], user_type='client')
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('Invalid client ID')

        try:
            quote = Quote.objects.get(id=data['quote_id'])
        except Quote.DoesNotExist:
            raise serializers.ValidationError('Invalid quote ID')

        # Ensure that the price is a positive number
        if data['price'] <= 0:
            raise serializers.ValidationError('Price must be a positive number')

        return data
