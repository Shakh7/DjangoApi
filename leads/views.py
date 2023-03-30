# Create your views here.
from rest_framework import permissions, generics
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from cars.models import Car, CarModel
from city.models import City
from customers.models import Customer
from .models import Lead as Lead
from .serializers import LeadSerializer as LeadSerializer


class LeadListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        todos = Lead.objects.all()
        serializer = LeadSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        print(request.data)
        data = {
            'task': request.data.get('task'),
            'completed': request.data.get('completed'),
            'user': request.user.id
        }
        serializer = LeadSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeadCreateView(generics.CreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    def create(self, request, *args, **kwargs):
        car_make_id = request.data.get('car_make')
        car_model_id = request.data.get('car_model')
        car_year = request.data.get('car_year')
        pick_up_address_id = request.data.get('pick_up_address')
        drop_off_address_id = request.data.get('drop_off_address')
        pick_up_date = request.data.get('pick_up_date')

        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')

        car_make = Car.objects.filter(id=car_make_id).first()
        car_model = CarModel.objects.filter(id=car_model_id).first()
        pick_up_address = City.objects.filter(id=pick_up_address_id).first()
        drop_off_address = City.objects.filter(id=drop_off_address_id).first()
        customer, _ = Customer.objects.get_or_create(first_name=first_name, last_name=last_name, email=email)

        if not car_make or not car_model or not pick_up_address or not drop_off_address:
            raise ValidationError("Invalid input data")

        if car_model not in car_make.models.all():
            raise ValidationError("Selected car model is not included in selected car's models.")

        lead = Lead(
            car_make=car_make,
            car_model=car_model,
            car_year=car_year,
            pick_up_address=pick_up_address,
            drop_off_address=drop_off_address,
            pick_up_date=pick_up_date,
            customer=customer
        )

        lead.save()
        serializer = self.get_serializer(lead)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
