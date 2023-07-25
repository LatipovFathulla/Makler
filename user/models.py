from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
import random
from django.utils import timezone
from django.contrib.sites.models import Site
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




class CustomUser(AbstractUser):
    username = None
    date_birth = models.DateField(null=True, blank=True)
    avatar_image = models.FileField(upload_to='custom_avatar_image', null=True, blank=True)
    phone_number = models.CharField(max_length=40, unique=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    mycode = models.IntegerField(null=True)
    is_premium = models.BooleanField(default=False)
    referrer = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    score = models.IntegerField(default=0)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = MyUserManager()

    def __str__(self):
        return f"{self.phone_number}"

    def generate_mycode(self):
        self.mycode = str(random.randint(1000, 9999))
        self.save(update_fields=['mycode'])
        return self.mycode

    def is_valid_mycode(self, mycode):
        return str(mycode) == str(self.mycode)

    def clear_mycode(self):
        self.mycode = None
        self.save(update_fields=['mycode'])

    def save(self, *args, **kwargs):
        if not self.mycode:
            self.mycode = str(random.randint(100000, 999999))
        # Удаление mycode через 2 дня
        if self.created_at and (timezone.now().date() - self.created_at) >= timezone.timedelta(days=2):
            self.mycode = None
        super().save(*args, **kwargs)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'id': str(self.id),
        }
