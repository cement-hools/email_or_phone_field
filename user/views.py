import csv

import tablib as tablib
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Statistic
from .serializers import (AddUserSerializer, StatisticSerializer,
                          LoginSerializer)
from .utils import make_random_password


@api_view(['GET'])
def logout_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        user_login = request.user.login
        logout(request)
        return Response(
            {'ok': f'пользователь {user_login} вышел из системы'},
            status=status.HTTP_200_OK)
    return Response({'unauthorized': 'пользователь не аутентифицирован'},
                    status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def login_view(request, *args, **kwargs):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user_login = request.data.get('login')
        user = serializer.validated_data.get('user')
        if user is not None:
            login(request, user)
            return Response(
                {'ok': f'пользователь {user.login} вошел в систему'},
                status=status.HTTP_200_OK)
        return Response(
            {'not found': f'пользователя login: {user_login}, нет в системе '
                          f'или неправильный пароль'},
            status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def adduser(request, *args, **kwargs):
    serializer = AddUserSerializer(data=request.data)
    if serializer.is_valid():
        print('valid')
        password = make_random_password()
        password_hash = make_password(password)
        serializer.save(password=password_hash)
        user_name = serializer.validated_data.get('name')
        user_login = serializer.validated_data.get('login')
        Statistic.objects.create(
            status='HTTP_201_CREATED',
            text=f'Пользователь {user_name} успешно создан',
        )
        response = {
            'login': user_login,
            'password': password,
        }
        return Response(response, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    code = {
        'unique': 'Пользователь с таким полем уже существует',
        'required': 'Обязательное поле',
        'invalid': 'Неверное значение',
    }
    error_dict = dict()
    for field, error in serializer.errors.items():
        print(error[0], error[0].code)
        if error[0].code in error_dict.keys():
            error_dict[error[0].code].append(field)
        else:
            error_dict[error[0].code] = [field]

    print(error_dict)
    text_list = []
    for k, v in error_dict.items():
        text_list.append(f'{code.get(k)} ({", ".join(v)})')
    print(text_list)
    error_text = ', '.join(text_list)

    Statistic.objects.create(
        status='HTTP_400_BAD_REQUEST',
        text=error_text,
    )
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def statistic(request, *args, **kwargs):
    statistic_set = Statistic.objects.all()
    serializer = StatisticSerializer(instance=statistic_set, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def export_excel(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stat.xls"'

    writer = csv.writer(response)
    writer.writerow(['create_date', 'status', 'text'])

    statistic_set = Statistic.objects.all().values_list('create_date',
                                                        'status', 'text')
    for row in statistic_set:
        writer.writerow(row)

    return response


@api_view(['GET'])
def export_txt(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stat.txt"'

    writer = csv.writer(response)
    writer.writerow(['create_date', 'status', 'text'])

    statistic_set = Statistic.objects.all().values_list('create_date',
                                                        'status', 'text')
    for row in statistic_set:
        writer.writerow(row)

    return response
