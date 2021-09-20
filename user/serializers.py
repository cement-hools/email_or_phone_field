from abc import ABC

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import User, Statistic


class AddUserSerializer(ModelSerializer):
    """Сериалайзер добавления пользователя."""

    date_of_birth = serializers.DateField(format="%d.%m.%Y",
                                          input_formats=['%d.%m.%Y'])

    class Meta:
        model = User
        exclude = ('password',)


class StatisticSerializer(ModelSerializer):
    """Сериалайзер добавления пользователя."""

    create_date = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")

    class Meta:
        model = Statistic
        exclude = ('id',)


class LoginSerializer(serializers.Serializer): # noqa
    login = serializers.CharField(max_length=128, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        login = data.get('login')
        password = data.get('password')

        if login is None:
            raise serializers.ValidationError(
                'An login address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(login=login, password=password)

        return {
            'user': user,
        }
