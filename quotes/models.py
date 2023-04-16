import requests
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from cars.models import Car, CarModel
from city.models import City
from django.core.exceptions import ValidationError
from customers.models import Customer
from users.models import CustomUser


class Quote(models.Model):
    car_make = models.ForeignKey(Car, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    car_year = models.IntegerField(max_length=4, validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    pick_up_address = models.ForeignKey(City, on_delete=models.CASCADE, related_name='pick_up_quotes')
    drop_off_address = models.ForeignKey(City, on_delete=models.CASCADE, related_name='drop_off_quotes')
    pick_up_date = models.DateField(default=timezone.now)
    is_operable = models.BooleanField(default=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='quotes')
    created_at = models.DateTimeField(auto_now_add=True)
    clients = models.ManyToManyField(CustomUser, related_name='quotes')

    is_lead = models.BooleanField(default=False)

    def clean(self):
        if self.car_model not in self.car_make.models.all():
            raise ValidationError("Selected car model is not included in selected car's models.")

    def save(self, *args, **kwargs):
        is_new_instance = not self.pk  # Check if this is a new instance or an update
        super().save(*args, **kwargs)
        if is_new_instance:
            text = f'New lead ✅: \n\n' \
                   f'Car Make: {self.car_make.name}\n' \
                   f'Car Model: {self.car_model.name}\n' \
                   f'Car Year: {self.car_year} \n' \
                   f'Pick Up: {self.pick_up_address.zip_code} {self.pick_up_address.city_name}, {self.pick_up_address.state_code}\n' \
                   f'Drop Off: {self.drop_off_address.zip_code} {self.drop_off_address.city_name}, {self.drop_off_address.state_code}\n' \
                   f'Pick Up Date: {self.pick_up_date} \n' \
                   f'Name: {self.customer.first_name} {self.customer.last_name}\n' \
                   f'Email: {self.customer.email} \n\n' \
                   f'Created At: {self.created_at}'
            response = requests.get(
                f'https://api.telegram.org/bot6170443565:AAGsnbPJfnLMWnTjHwth5O4hkosdQXb0O9E/sendMessage?chat_id=5000241789&text={text}&parse_mode=Markdown')

    def __str__(self):
        return self.car_make.name
