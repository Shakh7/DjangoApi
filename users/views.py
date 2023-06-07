from django.utils.crypto import get_random_string
from rest_framework import permissions, serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from helpers.auth import SessionAuthAPIListView, IsAdmin
from .models import CustomUser as Users
from .serializers import UserSerializer as UserSerializer

from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseBadRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.helpers import send_email_confirmation


class ClientListApiView(SessionAuthAPIListView):
    permission_classes = [IsAdmin]
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = Users.objects.filter(user_type='client')
        return queryset


class UserListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        todos = Users.objects.all()
        serializer = UserSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'task': request.data.get('task'),
            'completed': request.data.get('completed'),
            'user': request.user.id
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def confirm_email(request):
    return send_email_confirmation.confirm_email(request)
