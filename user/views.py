import csv

from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Statistic
from .serializers import (AddUserSerializer, StatisticSerializer,
                          LoginSerializer)
from .utils import (make_random_password, statistic_create_user,
                    statistic_not_create_user)

User = get_user_model()


@api_view(['POST'])
def logout_view(request, *args, **kwargs):
    """Выйти из системы."""
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
    """Войти в систему."""
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
    """Создать пользователя."""
    serializer = AddUserSerializer(data=request.data)
    if serializer.is_valid():
        password = make_random_password()
        password_hash = make_password(password)
        serializer.save(password=password_hash)
        user_name = serializer.validated_data.get('name')
        user_login = serializer.validated_data.get('login')

        statistic_create_user(user_name)

        response = {
            'login': user_login,
            'password': password,
        }
        return Response(response, status=status.HTTP_201_CREATED)

    statistic_not_create_user(serializer.errors)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def statistic(request, *args, **kwargs):
    """Статистика обращений к useradd/."""
    statistic_set = Statistic.objects.all()
    serializer = StatisticSerializer(instance=statistic_set, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def export_excel(request):
    """Экспорт статистики в xls."""
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
@permission_classes((IsAuthenticated,))
def export_txt(request):
    """Экспорт статистики в txt."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stat.txt"'

    writer = csv.writer(response)
    writer.writerow(['create_date', 'status', 'text'])

    statistic_set = Statistic.objects.all().values_list('create_date',
                                                        'status', 'text')
    for row in statistic_set:
        writer.writerow(row)

    return response
