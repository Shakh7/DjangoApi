from rest_framework import serializers
from .models import Vehicle, VehicleMake


class VehicleSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=100)
    year = serializers.IntegerField()
    make = serializers.SerializerMethodField(method_name='get_make')
    model = serializers.CharField(max_length=100)
    category = serializers.ChoiceField(choices=Vehicle.CATEGORY_CHOICES, default='sedan')

    def create(self, validated_data):
        print(validated_data)
        return Vehicle.objects.first()

    def update(self, instance, validated_data):
        instance.year = validated_data.get('year', instance.year)
        instance.make = validated_data.get('make', instance.make)
        instance.model = validated_data.get('model', instance.model)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance

    def get_make(self, obj):
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT'):
            return obj.make.id
        else:
            return {'id': obj.make.id, 'name': obj.make.name}


class VehicleMakeSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return VehicleMake.objects.first()

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
