from rest_framework import serializers


class LeadSerializer(serializers.Serializer):
    id = serializers.CharField()
    created_at = serializers.DateTimeField()
    client = serializers.SerializerMethodField(method_name="get_client")
    quote = serializers.SerializerMethodField(method_name="get_quote")
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    def get_client(self, lead):
        return lead.client.full_name

    def get_quote(self, lead):
        return lead.quote.id
