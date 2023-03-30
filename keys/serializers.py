from rest_framework import serializers

from leads.serializers import LeadSerializer as LeadSerializer
from users.serializers import UserSerializer
from .models import ApiKey as ApiKey


class ApiKeySerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    leads = LeadSerializer(many=True)

    class Meta:
        model = ApiKey
        fields = ["key", "user", "leads"]
