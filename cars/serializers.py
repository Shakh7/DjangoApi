from rest_framework import serializers
from .models import Car, CarModel
from rest_framework.serializers import ModelSerializer


class CarModelSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, read_only=True)
    series = serializers.CharField(max_length=100, read_only=True)


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    models = serializers.SerializerMethodField()

    def get_models(self, car):
        query = self.context.get('view').kwargs.get('search')
        models = car.models.all()
        if query and ((query.upper() in car.name.upper()) == False):
            print("ddddd")
            models = models.filter(name__icontains=query)
        return ModelSerializer(models, many=True).data

    class Meta:
        model = Car
        fields = '__all__'
