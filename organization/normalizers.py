from .models import Organization


def organizations_normalizer(data):
    result = []
    for organization in data:
        organization_details = Organization.objects.get(pk=organization['id'])

        item = {
            'id': organization['id'],
            'label': organization['label'],
            'description': organization['description'],
            'created_at': organization['created_at'],
            'updated_at': organization['updated_at'],
            'role': {
                'id': organization_details.role.id,
                'label': organization_details.role.label,
            } if organization_details.role else 'null',
        }

        result.append(item)

    return result


def organization_normalizer(data):
    return {
        'id': data.id,
        'label': data.label,
        'description': data.description,
        'created_at': data.created_at,
        'updated_at': data.updated_at,
        'role': {
            'id': data.role.id,
            'label': data.role.label,
        } if data.role else 'null',
    }
