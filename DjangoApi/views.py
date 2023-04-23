from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken
from users.models import CustomUser

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from django.http import JsonResponse


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            response.set_cookie('access_token',
                                response.data['access'], httponly=True,
                                secure=True, samesite='None')
        return response


class VerifyTokenView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]

    def get(self, request, *args, **kwargs):
        user = request.user
        return JsonResponse({'username': user.full_name, 'email': user.email})


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
            except InvalidToken:
                pass

        return response
