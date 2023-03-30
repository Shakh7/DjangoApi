from django.urls import path

from .views import (
    CarSearchView as CarSearchView,
    CarListView as CarListView,
)

urlpatterns = [
    path('cars/', CarListView.as_view()),
    path('cars/<str:search>/', CarSearchView.as_view()),
]
