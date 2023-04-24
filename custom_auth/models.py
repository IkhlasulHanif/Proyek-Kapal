from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    inspector = 'inspector'
    repairmen = 'repairmen'
    admin = 'admin'
    ROLE_CHOICES = [
        (inspector, 'Inspector'),
        (repairmen, 'Repairmen'),
        (admin, 'Admin'),
    ]
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=255, blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default=inspector)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

class Ship(models.Model):
    name = models.CharField(max_length=100)
    # other fields

class Block(models.Model):
    name = models.CharField(max_length=100)
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, related_name='blocks')
    # other fields