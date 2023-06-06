from django.contrib import admin

from customers.models import Customer
# Register your models here.
from .models import Quote


# Register your models here.

class QuoteAdmin(admin.ModelAdmin):
    model = Quote
    list_display = ('id', 'car_make', 'car_model', 'origin', 'destination',
                    'is_operable', 'shipper',
                    'created_at')


admin.site.register(Quote, QuoteAdmin)
