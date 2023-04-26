from django.contrib import admin
#
# from customers.models import Customer
# # Register your models here.
from .models import Lead


#
#
# # Register your models here.
#
class LeadAdmin(admin.ModelAdmin):
    model = Lead


admin.site.register(Lead, LeadAdmin)
