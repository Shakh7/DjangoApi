from django.contrib import admin

# Register your models here.

from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone']
    search_fields = ['first_name', 'last_name', 'email', 'phone']


admin.site.register(Customer, CustomerAdmin)
