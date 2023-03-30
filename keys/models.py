import random
import string

from django.db import models

from leads.models import Lead as Lead
from users.models import CustomUser as User


def number_default_function():
    N = 45
    res = ''.join(random.choices(string.ascii_letters +
                                 string.digits, k=N))
    return res


# Create your models here.

class ApiKey(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    key = models.CharField(
        max_length=100,
        blank=False,
        default=number_default_function,
        unique=True,
    )
    leads = models.ManyToManyField(Lead, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, default='active', max_length=100)

    def __str__(self):
        return self.key
