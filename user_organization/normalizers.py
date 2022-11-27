from .models import UserOrganization


def user_organizations_normalizer(data):
    result = []
    for user_organization in data:
        user_organization_details = UserOrganization.objects.get(pk=user_organization['id'])

        item = {
            'id': user_organization['id'],
            'organization': {
                'id': user_organization_details.organization.id,
                'label': user_organization_details.organization.label,
            },
            'user': {
                'id': user_organization_details.user.id,
                'firstname': user_organization_details.user.firstname,
                'lastname': user_organization_details.user.lastname,
                'email': user_organization_details.user.email,
            },
            'role': {
                'id': user_organization_details.role.id,
                'label': user_organization_details.role.label,
            },
        }

        result.append(item)

    return result


def user_organization_normalizer(data):
    return {
        'id': data['id'],
        'organization': {
            'id': data.organization.id,
            'label': data.organization.label,
        },
        'user': {
            'id': data.user.id,
            'firstname': data.user.firstname,
            'lastname': data.user.lastname,
            'email': data.user.email,
        },
        'role': {
            'id': data.role.id,
            'label': data.role.label,
        },
    }
