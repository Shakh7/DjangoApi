from django.db import models


# Create your models here.

class Car(models.Model):
    name = models.CharField(max_length=120, unique=True)
    models = models.ManyToManyField('CarModel', blank=True, null=True, related_name='cars')

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(max_length=120)
    series = models.CharField(max_length=120, default=None, blank=True, null=True)

    def __str__(self):
        return self.name
