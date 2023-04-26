from django.contrib import admin

from customers.models import Customer
# Register your models here.
from .models import Quote


# Register your models here.

class QuoteAdmin(admin.ModelAdmin):
    model = Quote
    list_display = ('id', 'customer', 'car_make', 'car_model', 'origin', 'destination', 'pick_up_date',
                    'is_operable', 'created_at')


admin.site.register(Quote, QuoteAdmin)
