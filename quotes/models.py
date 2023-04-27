import requests
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from cars.models import Car, CarModel
from city.models import City
from django.core.exceptions import ValidationError
from customers.models import Customer
from users.models import CustomUser
import uuid


class Quote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='quotes')
    pick_up_date = models.DateField(default=timezone.now)

    car_make = models.ForeignKey(Car, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    car_year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)])

    origin = models.ForeignKey(City, on_delete=models.CASCADE, related_name='origin')
    destination = models.ForeignKey(City, on_delete=models.CASCADE, related_name='destination')

    is_operable = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id'], name='unique_quote_id'),
        ]

    def clean(self):
        if self.car_model not in self.car_make.models.all():
            raise ValidationError("Selected car model is not included in selected car's models.")

    def save(self, *args, **kwargs):
        is_new_instance = not self.pk  # Check if this is a new instance or an update

        if is_new_instance:
            super().save(*args, **kwargs)
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
            requests.get(
                f'https://api.telegram.org/bot6170443565:AAGsnbPJfnLMWnTjHwth5O4hkosdQXb0O9E/sendMessage?chat_id=5000241789&text={text}&parse_mode=Markdown')
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.car_make.name + ', ' + self.car_model.name
