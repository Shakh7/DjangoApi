from rest_framework import serializers


class LeadSerializer(serializers.Serializer):
    id = serializers.CharField()
    created_at = serializers.DateTimeField()
    client = serializers.SerializerMethodField(method_name="get_client")
    quote = serializers.SerializerMethodField(method_name="get_quote")
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    def get_client(self, lead):
        return {
            'id': lead.client.id,
            'full_name': lead.client.full_name,
            'email': lead.client.email
        }

    def get_quote(self, lead):
        return {
            'id': lead.quote.id,
            'car_make': lead.quote.car_make.name,
            'car_model': lead.quote.car_model.name,
            'car_year': lead.quote.car_year,
            'customer': {
                'id': lead.quote.customer.id,
                'full_name': lead.quote.customer.full_name,
                'email': lead.quote.customer.email,
            }
        }
