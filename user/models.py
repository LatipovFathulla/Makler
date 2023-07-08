from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from django.core.exceptions import ValidationError


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone_number, password, **extra_fields):
        """
            Create and save a User with the given email and password.
            """
        if not phone_number:
            raise ValueError('The Email must be set')
        if not password:
            raise ValueError('The Password must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        """
            Create and save a SuperUser with the given email and password.
            """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone_number, password, **extra_fields)


import random


class CustomUser(AbstractUser):
    username = None
    date_birth = models.DateField(null=True, blank=True)
    avatar_image = models.FileField(upload_to='custom_avatar_image', null=True, blank=True)
    phone_number = models.CharField(max_length=40, unique=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    mycode = models.IntegerField(null=True)
    is_premium = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = MyUserManager()

    def __str__(self):
        return f"{self.phone_number}"

    @classmethod
    def mycode2(self):
        return random.randint(100000, 999999)

    def save(self, *args, **kwargs):
        self.mycode = self.mycode2()
        super().save(*args, **kwargs)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'id': str(self.id),
        }


