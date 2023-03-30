from django.contrib import admin

from .models import CustomUser as Users


# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    model = Users
    list_display = ['email', 'full_name', 'is_staff']


admin.site.register(Users, CustomUserAdmin)
