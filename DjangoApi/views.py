from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView
from django.http import JsonResponse


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            response.set_cookie('access_token',
                                response.data['access'], httponly=True,
                                secure=True, samesite='None')
        return response


class CustomTokenVerifyView(TokenVerifyView):
    def get(self, request, *args, **kwargs):
        # retrieve the access token from cookies
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return JsonResponse({'error': 'Access token not found'}, status=400)

        # pass the access token to TokenVerifyView to verify the token
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            # return user info from validated token
            return JsonResponse(response.data['user'], status=200)

        return JsonResponse({'error': 'Invalid token'}, status=401)
