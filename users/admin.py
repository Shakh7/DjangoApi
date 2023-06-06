from django.contrib import admin

from .models import CustomUser as Users

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    model = Users
    list_display = ['first_name', 'last_name', 'email', 'user_type']


admin.site.register(Users, CustomUserAdmin)
