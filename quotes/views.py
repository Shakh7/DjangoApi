from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from cars.models import Car, CarModel
from city.models import City
from customers.models import Customer
from .models import Quote as Quote
from .serializers import QuoteSerializer as QuoteSerializer
from helpers.auth import SessionAuthAPIListView, IsAdmin
from django.core.cache import cache
from django.db.models import Q, Count


class QuoteListApiView(SessionAuthAPIListView):
    permission_classes = [IsAdmin]
    serializer_class = QuoteSerializer
    cache_key = 'quote_list_cash'

    def get_queryset(self):
        queryset = cache.get(self.cache_key)

        if queryset is None:
            queryset = Quote.objects \
                .select_related('customer', 'car_make', 'car_model') \
                .prefetch_related('leads', 'origin', 'destination') \
                .order_by('-created_at')
            cache.set(self.cache_key, queryset)

        id = self.request.query_params.get('id')
        created_at = self.request.query_params.get('created_at')
        car_make = self.request.query_params.get('car_make')
        origin = self.request.query_params.get('origin')
        destination = self.request.query_params.get('destination')
        customer = self.request.query_params.get('customer')
        pick_up_date = self.request.query_params.get('pick_up_date')
        is_operable = self.request.query_params.get('is_operable')
        notes = self.request.query_params.get('notes')
        quote_clients_count = self.request.query_params.get('quote_clients')

        if id:
            queryset = queryset.filter(id__icontains=id)

        if created_at:
            queryset = queryset.filter(created_at__icontains=created_at)

        if car_make:
            queryset = queryset.filter(
                Q(car_make__name__icontains=car_make) |
                Q(car_model__name__icontains=car_make) |
                Q(car_year__icontains=car_make)
            )

        if origin:
            queryset = queryset.filter(
                Q(origin__zip_code__icontains=origin) |
                Q(origin__city_name__icontains=origin) |
                Q(origin__state_code__icontains=origin) |
                Q(origin__state_name__icontains=origin)
            )

        if destination:
            queryset = queryset.filter(
                Q(destination__zip_code__icontains=destination) |
                Q(destination__city_name__icontains=destination) |
                Q(destination__state_code__icontains=destination) |
                Q(destination__state_name__icontains=destination)
            )

        if customer:
            queryset = queryset.filter(
                Q(customer__full_name__icontains=customer) |
                Q(customer__email__icontains=customer)
            )

        if pick_up_date:
            queryset = queryset.filter(pick_up_date__icontains=pick_up_date)

        if is_operable:
            query = True if is_operable == 'yes' else False
            queryset = queryset.filter(is_operable=query)

        if notes:
            queryset = queryset.filter(notes__icontains=notes)

        if quote_clients_count:
            leads = queryset.annotate(num_leads=Count('leads'))
            queryset = leads.filter(num_leads__icontains=quote_clients_count)

        limit = self.request.query_params.get('limit')
        offset = self.request.query_params.get('offset')

        if limit and offset:
            lim = int(limit.rstrip('/'))
            off = int(offset.rstrip('/'))
            queryset = queryset[lim:off + lim]
        elif offset:
            off = int(offset.rstrip('/'))
            queryset = queryset[off:]
        elif limit:
            lim = int(limit.rstrip('/'))
            queryset = queryset[:lim]

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
