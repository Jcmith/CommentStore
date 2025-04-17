from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    currency = models.CharField(max_length=3, choices=[
        ('GBP', 'British Pound Sterling'),
        ('EUR', 'Euro'),
        ('USD', 'US Dollars')
    ])


