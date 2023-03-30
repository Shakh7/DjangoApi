from django.contrib import admin

from .models import ApiKey as ApiKeys


# Register your models here.

class ApiKeysAdmin(admin.ModelAdmin):
    model = ApiKeys
    list_display = ['key', 'user', 'status']


admin.site.register(ApiKeys, ApiKeysAdmin)
