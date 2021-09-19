import hashlib
import hmac
import secrets
import warnings

from django.utils.deprecation import RemovedInDjango40Warning

NOT_PROVIDED = object()
RANDOM_STRING_CHARS = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'


def make_random_password(length=10, allowed_chars=RANDOM_STRING_CHARS):
    if length is NOT_PROVIDED:
        warnings.warn(
            'Not providing a length argument is deprecated.',
            RemovedInDjango40Warning,
        )
        length = 12
    return ''.join(secrets.choice(allowed_chars) for i in range(length))
