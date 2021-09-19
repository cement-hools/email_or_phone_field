from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from user_stat import settings
from .managers import UserManager


class CustomUser(models.Model):
    name = models.CharField('ФИО', max_length=128)

    email = models.EmailField('email', unique=True, blank=True)
    phone = models.PositiveIntegerField('телефон', unique=True, blank=True)

    date_of_birth = models.DateTimeField('дата рождения', blank=True,
                                         null=True)

    login = models.CharField('login', max_length=128, unique=True)
    password = models.CharField('password', max_length=128)

    date_joined = models.DateTimeField('registered', auto_now_add=True)

    is_active = True

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User'


class Status(models.TextChoices):
    TELEGRAM = "telegram"
    WHATSAPP = "whatsapp"


class Statistic(models.Model):
    status = models.CharField(max_length=255, blank=True,)
    text = models.CharField(max_length=255, blank=True)
    create_date = models.DateTimeField('', auto_now_add=True)

    class Meta:
        ordering = ('create_date',)

    def __str__(self):
        return f'{self.status}: {self.text}  {self.create_date.date()}'
