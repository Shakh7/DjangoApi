from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat


# Create your models here.

class City(models.Model):
    zip_code = models.IntegerField()
    city_name = models.CharField(max_length=100, db_index=True)
    state_code = models.CharField(max_length=10, db_index=True)
    state_name = models.CharField(max_length=100, db_index=True)
    geo_point = models.CharField(max_length=100, db_index=True)

    class Meta:
        unique_together = ('zip_code', 'city_name', 'state_name')

    def get_full_name(self):
        return f"{self.zip_code} {self.city_name} {self.state_code} {self.state_name}"

    @staticmethod
    def search(query):
        return City.objects.annotate(
            full_name=Concat(
                F('zip_code'), Value(' '), F('city_name'), Value(', '),
                F('state_name'), Value(', '), F('state_code'),
                output_field=models.TextField(),
            )
        ).filter(full_name__icontains=query)

    def __str__(self):
        return self.city_name + ', ' + self.state_code
