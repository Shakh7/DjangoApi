# Create your views here.
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from helpers.auth import IsAdmin
from .models import ApiKey as ApiKey
from .serializers import ApiKeySerializer as ApiKeySerializer


class ApiKeyListView(generics.ListAPIView):
    queryset = ApiKey.objects.all()
    serializer_class = ApiKeySerializer
    permission_classes = [IsAdmin, permissions.IsAuthenticated]


class ApiKeyDetailView(generics.RetrieveAPIView):
    lookup_field = 'key'
    queryset = ApiKey.objects.all()
    serializer_class = ApiKeySerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user or request.user.is_superuser:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({"detail": "Not found"})


class ApiKeyUpdateView(generics.UpdateAPIView):
    lookup_field = 'key'
    queryset = ApiKey.objects.all()
    serializer_class = ApiKeySerializer
    permission_classes = [IsAdmin, permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Api key updated successfully"})

        else:
            return Response({"message": "failed", "details": serializer.errors})
