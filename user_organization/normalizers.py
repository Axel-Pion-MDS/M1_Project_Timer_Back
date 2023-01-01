from .models import UserOrganization


def user_organizations_normalizer(data):
    result = []
    user_organization_parsed = []

    for user_organization in data:
        user_organization_details = UserOrganization.objects.get(pk=user_organization['id'])
        members = UserOrganization.objects.filter(organization_id=user_organization_details.organization.id)

        users = []
        if not (user_organization_details.organization.id in user_organization_parsed):
            user_organization_parsed.append(user_organization_details.organization.id)
            member_parsed = []
            for member in members:
                if not (member.user.id in member_parsed):
                    member_parsed.append(member.user.id)
                    users.append({
                        'id': member.user.id,
                        'firstname': member.user.firstname,
                        'lastname': member.user.lastname,
                        'email': member.user.email,
                        'role': {
                            'id': member.role.id,
                            'label': member.role.label,
                        },
                    })

            result.append({
                'id': user_organization['id'],
                'organization': {
                    'id': user_organization_details.organization.id,
                    'label': user_organization_details.organization.label,
                },
                'users': users
                if users else 'null'
            })

    return result


def user_organization_normalizer(data):
    members = []
    users_from_organization = UserOrganization.objects.filter(organization=data.organization.id)

    for member in users_from_organization:
        members.append({
            'id': member.user.id,
            'firstname': member.user.firstname,
            'lastname': member.user.lastname,
            'email': member.user.email,
            'role': {
                'id': member.role.id,
                'label': member.role.label,
            },
        })

    return {
        'id': data.id,
        'organization': {
            'id': data.organization.id,
            'label': data.organization.label,
        },
        'users': members if members else 'null'
    }


def users_from_organization_normalizer(data, organization):
    result = [{
        'organization': {
            'id': organization.id,
            'label': organization.label,
        }
    }]

    users = []
    for user in data:
        users.append({
            'id': user.user.id,
            'firstname': user.user.firstname,
            'lastname': user.user.lastname,
            'email': user.user.email,
            'role': {
                'id': user.role.id,
                'label': user.role.label,
            },
        })

    result.append({
        'users': users if users else 'null'
    })

    return result
