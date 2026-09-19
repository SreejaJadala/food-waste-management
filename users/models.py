from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN="ADMIN","Admin"
        PROVIDER="PROVIDER","Food Provider"
        NGO="NGO","NGO / Volunteer"
    role=models.CharField(max_length=12,choices=Role.choices,default=Role.PROVIDER)
