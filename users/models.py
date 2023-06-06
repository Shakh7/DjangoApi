from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ('super_admin', 'SuperAdmin'),  # is a super admin
        ('admin', 'Admin'),  # is a person who manages the system
        ('client', 'Client'),  # is a person who buys quotes
        ('shipper', 'Shipper'),  # is a person who leaves quotes
    )
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(_("first name"), max_length=80, blank=True)
    last_name = models.CharField(_("last name"), max_length=80, blank=True)
    email = models.EmailField(_("email address"), blank=True, null=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPES, default='admin')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, editable=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
