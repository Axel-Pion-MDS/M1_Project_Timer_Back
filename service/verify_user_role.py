from django.http import JsonResponse

from app import settings


def has_role(user_role, roles=('ROLE_ADMIN', 'ROLE_SUPER_ADMIN'), message='You do not have the privilege access for this resource.'):
    for role in roles:
        if user_role == settings.ROLES[role]:
            return True

    return JsonResponse({
        'code': settings.HTTP_CONSTANTS['FORBIDDEN'],
        'result': 'error',
        'message': message
    })
