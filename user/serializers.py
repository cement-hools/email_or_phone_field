from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import CustomUser, Statistic


class AddUserSerializer(ModelSerializer):
    """Сериалайзер добавления пользователя."""

    date_of_birth = serializers.DateField(format="%d.%m.%Y",
                                          input_formats=['%d.%m.%Y'])

    class Meta:
        model = CustomUser
        exclude = ('password',)


class StatisticSerializer(ModelSerializer):
    """Сериалайзер добавления пользователя."""

    create_date = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")

    class Meta:
        model = Statistic
        exclude = ('id',)
