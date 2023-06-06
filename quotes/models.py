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
    DELIVERY_CHOICES = (
        ('within_a_week', 'With in a week'),
        ('specific_date', 'Specific Date'),
        ('between_dates', 'Between Dates'),
        ('flexible', 'Flexible'),
        ('no_date', 'No date'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    delivery_choice = models.CharField(max_length=50, choices=DELIVERY_CHOICES, default='no_date')

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    car_make = models.ForeignKey(Car, on_delete=models.CASCADE, db_index=True)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, db_index=True)
    car_year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    origin = models.ForeignKey(City, on_delete=models.CASCADE, related_name='origin', db_index=True)
    destination = models.ForeignKey(City, on_delete=models.CASCADE, related_name='destination', db_index=True)
    is_operable = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)

    shipper = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name='quotes',
        db_index=True,
        null=True,
        blank=True,
        limit_choices_to={'user_type': 'shipper'}
    )

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
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError("End date must be greater than start date.")

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
