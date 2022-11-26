from .models import Role


def roles_normalizer(data):
    result = []
    for role in data:
        item = {
            'id': role['id'],
            'label': role['label'],
        }

        result.append(item)

    return result


def role_normalizer(data):
    return {
        'id': data.id,
        'label': data.label,
    }
