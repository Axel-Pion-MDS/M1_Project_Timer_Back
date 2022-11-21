from .models import User


def users_normalizer(data):
    result = []
    for user in data:

        item = {
            'id': user['id'],
            'firstname': user['firstname'],
            'lastname': user['lastname'],
            'email': user['email'],
            'password': user['password'],
            'created_at': user['created_at'],
            'updated_at': user['updated_at'],
        }

        result.append(item)

    return result


def user_normalizer(data):
    return {
        'id': data.id,
        'firstname': data.firstname,
        'lastname': data.lastname,
        'email': data.email,
        'password': data.password,
        'created_at': data.created_at,
        'updated_at': data.updated_at,
    }
