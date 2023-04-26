from django.urls import path

from .views import (
    QuoteListApiView, QuoteCreateView, QuoteDetailsApiView
)

urlpatterns = [
    path('quotes/', QuoteListApiView.as_view()),
    path('quotes/<int:id>/', QuoteDetailsApiView.as_view()),
    path('quotes/create/', QuoteCreateView.as_view()),
]




