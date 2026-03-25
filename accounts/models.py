from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class UserType(models.TextChoices):
        UNIVERSITY = 'university', 'University'
        COMPANY = 'company', 'Company'
        INVESTOR = 'investor', 'Investor'

    user_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.UNIVERSITY)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # keep username for admin compatibility

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        full = f"{self.first_name} {self.last_name}".strip()
        return full if full else self.email
