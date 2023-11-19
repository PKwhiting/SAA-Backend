from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_seller = models.BooleanField(default=False, blank=True, null=True)
    is_buyer = models.BooleanField(default=False, blank=True, null=True)
    is_admin = models.BooleanField(default=False, blank=True, null=True)
