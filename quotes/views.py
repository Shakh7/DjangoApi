# Create your views here.
from django.db.models import Q
from rest_framework import permissions
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from cars.models import Car, CarModel
from city.models import City
from customers.models import Customer
from .models import Quote as Quote
from .serializers import QuoteSerializer as QuoteSerializer
from datetime import datetime


class QuoteListApiView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuoteSerializer
    # authentication_classes = [BasicAuthentication]

    def get_queryset(self):
        queryset = Quote.objects \
            .select_related('car_make', 'customer') \
            .prefetch_related('clients') \
            .order_by('-created_at')

        query = self.request.query_params
        customer = query.get('customer')
        car_query_param = query.get('car')
        pick_up_address = query.get('pick_up_address')
        drop_off_address = query.get('drop_off_address')
        pick_up_date = query.get('pick_up_date')
        created_at = query.get('created_at')
        is_lead = query.get('is_lead')

        if customer:
            queryset = queryset.filter(customer__first_name__icontains=customer)

        if pick_up_address:
            queryset = queryset.filter(
                Q(pick_up_address__city_name__icontains=pick_up_address) |
                Q(pick_up_address__state_code__icontains=pick_up_address) |
                Q(pick_up_address__zip_code__icontains=pick_up_address)
            )

        if drop_off_address:
            queryset = queryset.filter(
                Q(drop_off_address__city_name__icontains=drop_off_address) |
                Q(drop_off_address__state_code__icontains=drop_off_address) |
                Q(drop_off_address__zip_code__icontains=drop_off_address)
            )

        if car_query_param:
            queryset = queryset.filter(
                Q(car_make__name__icontains=car_query_param) | Q(car_model__name__icontains=car_query_param))

        if is_lead:
            quote_status = True if is_lead == 'true' else False
            queryset = queryset.filter(is_lead=quote_status)

        if pick_up_date:
            queryset = queryset.filter(pick_up_date=pick_up_date)

        if created_at:
            date = datetime.strptime(created_at, '%Y-%m-%d').date()
            queryset = queryset.filter(created_at=date)

        return queryset


class QuoteCreateView(CreateAPIView):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        car_make_id = data.get('car_make')
        car_model_id = data.get('car_model')
        car_year = data.get('car_year')
        print("car_year", request.data)
        pick_up_address_id = data.get('pick_up_address')
        drop_off_address_id = data.get('drop_off_address')
        pick_up_date = data.get('pick_up_date')

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')

        car_make = Car.objects.filter(id=car_make_id).first()
        car_model = CarModel.objects.filter(id=car_model_id).first()
        pick_up_address = City.objects.filter(id=pick_up_address_id).first()
        drop_off_address = City.objects.filter(id=drop_off_address_id).first()
        customer, _ = Customer.objects.get_or_create(first_name=first_name, last_name=last_name, email=email)

        if not car_make or not car_model or not pick_up_address or not drop_off_address:
            raise ValidationError("Invalid input data")

        if car_model not in car_make.models.all():
            raise ValidationError("Selected car model is not included in selected car's models.")

        quote = Quote(
            car_make=car_make,
            car_model=car_model,
            car_year=car_year,
            pick_up_address=pick_up_address,
            drop_off_address=drop_off_address,
            pick_up_date=pick_up_date,
            customer=customer
        )
        quote.save()

        serializer = self.get_serializer(quote)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


class QuoteDetailsApiView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
