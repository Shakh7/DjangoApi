from django.contrib import admin

from .models import Car, CarModel


# Register your models here.

class CarAdmin(admin.ModelAdmin):
    model = Car
    list_display = ['id', 'name']
    search_fields = ['name']


class CarModelAdmin(admin.ModelAdmin):
    model = CarModel
    list_display = ['name']
    search_fields = ['name']


admin.site.register(Car, CarAdmin)
admin.site.register(CarModel, CarModelAdmin)
