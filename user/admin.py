from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import check_password, make_password

from user.models import User, Statistic


@admin.register(User)
class CustomUserAdmin(ModelAdmin):

    def save_model(self, request, obj, form, change):
        user_database = User.objects.get(pk=obj.pk)
        if not (check_password(form.data['password'],
                               user_database.password) or user_database.password ==
                form.data['password']):
            obj.password = make_password(obj.password)
        else:
            obj.password = user_database.password
        super().save_model(request, obj, form, change)


# admin.site.register(User)

admin.site.register(Statistic)
