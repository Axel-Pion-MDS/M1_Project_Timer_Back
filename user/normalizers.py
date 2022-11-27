from .models import User


def users_normalizer(data):
    result = []
    for user in data:
        user_details = User.objects.get(pk=user['id'])

        item = {
            'id': user['id'],
            'firstname': user['firstname'],
            'lastname': user['lastname'],
            'email': user['email'],
            'created_at': user['created_at'],
            'updated_at': user['updated_at'],
            'role': {
                'id': user_details.role.id,
                'label': user_details.role.label
            } if user_details.role else 'null'
        }

        result.append(item)

    return result


def user_normalizer(data):
    return {
        'id': data.id,
        'firstname': data.firstname,
        'lastname': data.lastname,
        'email': data.email,
        'created_at': data.created_at,
        'updated_at': data.updated_at,
        'role': {
                'id': data.role.id,
                'label': data.role.label
        } if data.role else 'null'
    }
