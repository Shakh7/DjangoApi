from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
import random
import string
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ('super_admin', 'SuperAdmin'),  # is a super admin
        ('admin', 'Admin'),  # is a person who manages the system
        ('client', 'Client'),  # is a person who buys quotes
        ('shipper', 'Shipper'),  # is a person who leaves quotes
    )
    username = models.CharField(max_length=220, unique=True)
    first_name = models.CharField(_("first name"), max_length=80, blank=True)
    last_name = models.CharField(_("last name"), max_length=80, blank=True)
    email = models.EmailField(_("email address"))
    user_type = models.CharField(max_length=50, choices=USER_TYPES, default='admin')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, editable=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.generate_username()
        if not self.password:
            self.set_password(generate_random_password())
        return super().save(*args, **kwargs)

    def generate_username(self):
        username = f"{self.first_name.lower()}_{self.last_name.lower()}_{self.email}"
        return username.replace(" ", "")

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email


def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    try:
        validate_password(password)
    except ValidationError:
        return generate_random_password(length)
    return password
