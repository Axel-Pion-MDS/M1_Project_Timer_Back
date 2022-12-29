import jwt
from django.conf import settings


def decode_token(authorization, secret_key=settings.TOKEN_KEY, algorithms='HS256'):
    token = str.replace(str(authorization), 'Bearer ', '')
    try:
        decode = jwt.decode(token, secret_key, algorithms)
    except jwt.DecodeError:
        return 1
    except jwt.InvalidTokenError:
        return 2

    return decode
