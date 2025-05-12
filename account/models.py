from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    fullName = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username
