from user_organization.models import UserOrganization
from .models import User


def users_normalizer(data):
    result = []
    for user in data:
        user_details = User.objects.get(pk=user['id'])
        organization_details = UserOrganization.objects.filter(user=user['id'])

        organizations = []
        for organization in organization_details:
            item = {
                'id': organization.organization.id,
                'label': organization.organization.label
            }

            organizations.append(item)

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
            } if user_details.role else 'null',
            'organizations': organizations if organizations else 'null',

        }

        result.append(item)

    return result


def user_normalizer(data):
    organization_details = UserOrganization.objects.filter(user=data.id)

    organizations = []
    for organization in organization_details:
        item = {
            'id': organization.organization.id,
            'label': organization.organization.label
        }

        organizations.append(item)

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
        } if data.role else 'null',
        'organizations': organizations if organizations else 'null',
    }
