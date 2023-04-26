from datetime import datetime

from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from users.models import CustomUser
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response


class CustomTokenVerifyView(TokenVerifyView):
    authentication_classes = (JWTAuthentication,)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = request.data.get('token', None)

        if token is not None:
            try:
                decoded_token = JWTAuthentication.get_validated_token(self, token)
                user_id = decoded_token['user_id']
                user = CustomUser.objects.get(id=user_id)
                user_info = {
                    'id': user.id,
                    'full_name': user.full_name,
                    'user_type': user.user_type,
                    'email': user.email
                }
                response.data['user'] = user_info
                response.data['access'] = token
                response.data['exp'] = decoded_token['exp']
            except InvalidToken:
                pass

        return response
