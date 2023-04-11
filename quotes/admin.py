from django.contrib import admin

# Register your models here.
from .models import Quote


# Register your models here.

class QuoteAdmin(admin.ModelAdmin):
    model = Quote


admin.site.register(Quote, QuoteAdmin)
