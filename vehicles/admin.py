from django.contrib import admin
from .models import Vehicle, VehicleMake


# Register your models here.

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'make', 'model', 'category')
    search_fields = ('year', 'make__name', 'model', 'category')
    list_filter = ('category', 'year', )
    list_per_page = 24


class VehicleMakeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_per_page = 25


admin.site.register(VehicleMake, VehicleMakeAdmin)
admin.site.register(Vehicle, VehicleAdmin)
