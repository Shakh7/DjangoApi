from django.urls import path

from .views import (
    CityListView as CityListView,
    CitySearchView as CitySearchView,
)

urlpatterns = [
    path('cities/', CityListView.as_view()),
    path('cities/<str:search>/', CitySearchView.as_view()),
]
