import csv

import tablib as tablib
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Statistic
from .serializers import AddUserSerializer, StatisticSerializer
from .utils import make_random_password


@api_view(['POST'])
def adduser(request, *args, **kwargs):
    password = make_random_password()
    password_hash = make_password(password)
    print(request.data)
    serializer = AddUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(password=password_hash)
        user_name = serializer.validated_data.get('name')
        login = serializer.validated_data.get('login')
        Statistic.objects.create(
            status='HTTP_201_CREATED',
            text=f'Пользователь {user_name} успешно создан',
        )
        response = {
            'login': login,
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

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def statistic(request, *args, **kwargs):
    statistic_set = Statistic.objects.all()
    serializer = StatisticSerializer(instance=statistic_set, many=True)
    return Response(serializer.data)


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
