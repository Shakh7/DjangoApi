from django.db import models
from quotes.models import Quote
from users.models import CustomUser


class Lead(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='leads', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='leads',
        limit_choices_to={'user_type': 'client'},
        blank=True, null=True
    )

    class Meta:
        unique_together = ('quote', 'client')

    def __str__(self):
        return \
                str(self.quote.car_model.name) + ', ' + \
                str(self.quote.car_make.name) + ' - ' + \
                str(self.client.email) + ' - $' + str(self.price)
