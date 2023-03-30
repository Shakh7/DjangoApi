from rest_framework import serializers


class CitySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    zip_code = serializers.IntegerField(read_only=True)
    city_name = serializers.CharField(max_length=100)
    state_code = serializers.CharField(max_length=100)
    state_name = serializers.CharField(max_length=100)
    geo_point = serializers.CharField(max_length=100)
