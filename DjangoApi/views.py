from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta
from django.contrib.auth import authenticate

import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class UserInfoView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        token = request.auth
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.SIMPLE_JWT['ALGORITHM']])
        user_id = decoded_token['user_id']
        user = User.objects.get(id=user_id)
        return Response({'email': user.email, 'username': user.username})


class TokenObtainPairView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=400)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response()
        # Store the tokens in cookies
        access_token_lifetime = int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds() / 60)
        response.set_cookie('access_token', access_token, httponly=True,
                            expires=datetime.utcnow() + timedelta(minutes=access_token_lifetime))
        refresh_token_lifetime = int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds() / 60 / 60 / 24)
        response.set_cookie('refresh_token', refresh_token, httponly=True,
                            expires=datetime.utcnow() + timedelta(days=refresh_token_lifetime))
        return response


class TokenRefreshView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'error': 'Refresh token is missing'}, status=400)

        try:
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)

            response = Response({'access_token': access_token})

            # Set new access token in cookies
            access_token_lifetime = int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds() / 60)
            response.set_cookie('access_token', access_token, httponly=True,
                                expires=datetime.utcnow() + timedelta(minutes=access_token_lifetime))

            return response

        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=400)
