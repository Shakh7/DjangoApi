import requests
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from cars.models import Car, CarModel
from city.models import City
from django.core.exceptions import ValidationError
from users.models import CustomUser
from users.models import CustomUser
import uuid
from django.core.cache import cache
from helpers.telegram import notify_new_quote


class Quote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    pick_up_date = models.DateField(default=timezone.now, null=True, blank=True)
    car_make = models.ForeignKey(Car, on_delete=models.CASCADE, db_index=True)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, db_index=True)
    car_year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    origin = models.ForeignKey(City, on_delete=models.CASCADE, related_name='origin', db_index=True)
    destination = models.ForeignKey(City, on_delete=models.CASCADE, related_name='destination', db_index=True)
    is_operable = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)

    first_name = models.CharField(max_length=80, blank=True, null=True)
    last_name = models.CharField(max_length=80, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id'], name='unique_quote_id'),
        ]
        indexes = [
            models.Index(fields=['car_make', 'car_model', 'origin', 'destination']),
        ]

    def clean(self):
        if self.car_model not in self.car_make.models.all():
            raise ValidationError("Selected car model is not included in selected car's models.")

    def save(self, *args, **kwargs):
        is_new_instance = self.pk

        if is_new_instance:
            super().save(*args, **kwargs)
            notify_new_quote(self)
        else:
            super().save(*args, **kwargs)

        cache.delete('quote_list_cash')

    def __str__(self):
        return self.car_make.name + ', ' + self.car_model.name
