import jwt


# TODO: replace secret_key and algorithms with env variables
def decode_token(authorization, secret_key='ProjectTimer', algorithms='HS256'):
    token = str.replace(str(authorization), 'Bearer ', '')
    return jwt.decode(token, secret_key, algorithms)
