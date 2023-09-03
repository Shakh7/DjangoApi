from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, VehicleMakeViewSet, VehicleRegisterViewSet

router = DefaultRouter()
router.register('vehicles', VehicleViewSet)
router.register('makes', VehicleMakeViewSet, basename='vehicle_make')
router.register('models', VehicleMakeViewSet, basename='vehicle_model')
router.register('register', VehicleRegisterViewSet, basename='vehicle_register')

urlpatterns = [
    path('', include(router.urls)),
]
