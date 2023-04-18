from django.db import models
from quotes.models import Quote
from users.models import CustomUser


class Lead(models.Model):

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.quote:
            return self.quote

    @property
    def get_customer_count(self):
        return self.client.all().count()
