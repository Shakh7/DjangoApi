from rest_framework import serializers

from .models import CustomUser as Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'full_name', 'email', 'date_joined']
