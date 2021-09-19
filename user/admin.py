from django.contrib import admin
from django.contrib.auth import get_user_model

from user.models import CustomUser, Statistic

admin.site.register(CustomUser)
admin.site.register(Statistic)
