from django.db import models
from django.contrib.auth.models import AbstractUser as AbstactUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class User(AbstactUser):
    phone_number = PhoneNumberField(unique=True, null=False, blank=False)

    def __str__(self):
        return self.phone_number


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField(null=True, blank=True)
