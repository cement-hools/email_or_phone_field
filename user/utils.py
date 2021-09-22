import hashlib
import hmac
import secrets
import warnings

from django.utils.deprecation import RemovedInDjango40Warning

from user.models import Statistic

NOT_PROVIDED = object()
RANDOM_STRING_CHARS = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'

CODE = {
    'unique': 'Пользователь с таким полем уже существует',
    'required': 'Обязательное поле',
    'invalid': 'Неверное значение',
}


def make_random_password(length=10, allowed_chars=RANDOM_STRING_CHARS):
    if length is NOT_PROVIDED:
        warnings.warn(
            'Not providing a length argument is deprecated.',
            RemovedInDjango40Warning,
        )
        length = 12
    return ''.join(secrets.choice(allowed_chars) for i in range(length))


def statistic_create_user(name):
    """Добавить в статистику информацию о созданном пользователе."""
    Statistic.objects.create(
        status='HTTP_201_CREATED',
        text=f'Пользователь {name} успешно создан',
    )


def statistic_not_create_user(errors):
    """Добавить в статистику информацию об ошибках
    при создании пользователя."""
    error_dict = dict()
    for field, error in errors.items():
        if error[0].code in error_dict.keys():
            error_dict[error[0].code].append(field)
        else:
            error_dict[error[0].code] = [field]
    text_list = []
    for k, v in error_dict.items():
        text_list.append(f'{CODE.get(k)} ({", ".join(v)})')

    error_text = ', '.join(text_list)

    Statistic.objects.create(
        status='HTTP_400_BAD_REQUEST',
        text=error_text,
    )
