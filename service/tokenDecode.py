import jwt
from django.conf import settings


def decode_token(authorization, secret_key=settings.TOKEN_KEY, algorithms='HS256'):
    token = str.replace(str(authorization), 'Bearer ', '')
    return jwt.decode(token, secret_key, algorithms)
