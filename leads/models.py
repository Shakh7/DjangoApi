from django.db import models
from quotes.models import Quote
from users.models import CustomUser


class Lead(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='leads', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    client = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('quote', 'client',)

    def __str__(self):
        return self.quote.__str__() + ' -- $' + str(self.price)

    # @property
    # def get_customer_count(self):
    #     return self.client.all().count()
