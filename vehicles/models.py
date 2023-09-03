from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomIDField(models.UUIDField):
    def __init__(self, *args, **kwargs):
        kwargs['default'] = uuid.uuid4
        kwargs['editable'] = False
        kwargs['unique'] = True
        kwargs['primary_key'] = True
        super().__init__(*args, **kwargs)


class VehicleMake(TimestampedModel):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def search_name(self, search_name):
        self_name_lower = self.name.lower()
        search_name_lower = search_name.lower()

        return search_name_lower == self_name_lower

    def __str__(self):
        return self.name


class Vehicle(TimestampedModel):
    CATEGORY_CHOICES = (
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('van', 'Van'),
        ('Van/Minivan', 'Van/Minivan'),
        ('Pickup', 'Pickup'),
        ('other', 'Other'),
        ('Hatchback', 'Hatchback'),
        ('Wagon', 'Wagon'),
        ('Coupe', 'Coupe'),

    )
    id = CustomIDField()
    year = models.PositiveIntegerField(
        null=False, blank=False,
        db_index=True,
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(timezone.now().year)
        ]
    )
    make = models.ForeignKey(VehicleMake, on_delete=models.CASCADE, related_name='vehicles', null=False, blank=False,
                             db_index=True)
    model = models.CharField(max_length=100, null=False, blank=False, db_index=True)
    category = models.CharField(
        max_length=100, choices=CATEGORY_CHOICES, default='other',
        db_index=True
    )

    def __str__(self):
        return str(self.id)
