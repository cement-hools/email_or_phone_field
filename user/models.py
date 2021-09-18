from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from user.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField('ФИО', max_length=128)

    email = models.EmailField('email', unique=True, blank=True)
    phone = models.PositiveIntegerField('телефон', unique=True, blank=True)
    born = models.DateTimeField('дата рождения', blank=True)

    login = name = models.CharField('login', max_length=128, unique=True)

    date_joined = models.DateTimeField('registered', auto_now_add=True)
    is_active = models.BooleanField('is_active', default=True)

    objects = UserManager()

    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
