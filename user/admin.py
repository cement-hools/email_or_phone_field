from django.contrib import admin
from django.contrib.auth import get_user_model

from user.models import User, Statistic

admin.site.register(User)
admin.site.register(Statistic)
