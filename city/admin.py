from django.contrib import admin

from .models import City as Cities


# Register your models here.

class CityAdmin(admin.ModelAdmin):
    model = Cities
    list_display = ['zip_code', 'city_name', 'state_code', 'state_name', 'geo_point']
    search_fields = ['zip_code', 'city_name', 'state_code', 'state_name']


admin.site.register(Cities, CityAdmin)
