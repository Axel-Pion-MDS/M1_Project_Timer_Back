import django.middleware.csrf
import json

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from service import tokenDecode
from user.models import User
from .models import Role
from .normalizers import role_normalizer, roles_normalizer
from .forms import RoleForm


# @csrf_protect
@csrf_exempt
def get_roles(request):
    if request.method != 'GET':
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'error',
            'message': 'Must be a GET method',
        })

    try:
        authorization = request.headers.get('Authorization')
        jwt_content = tokenDecode.decode_token(authorization)
        if isinstance(jwt_content, int):
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
                'result': 'error',
                'message': 'An error has occurred while decoding the JWT Token.'
                if jwt_content == 1 else 'JWT Token invalid.'
            })

        User.objects.get(pk=jwt_content.get('id'))
    except User.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'User not found.'
        })

    try:
        roles = Role.objects.all().values()
    except Role.DoesNotExist:
        return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': []})

    data = roles_normalizer(roles)
    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': data})


@csrf_exempt
def get_role(request, role_id):
    if request.method != "GET":
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'error',
            'message': 'Must be a GET method',
        })

    try:
        authorization = request.headers.get('Authorization')
        jwt_content = tokenDecode.decode_token(authorization)
        if isinstance(jwt_content, int):
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
                'result': 'error',
                'message': 'An error has occurred while decoding the JWT Token.'
                if jwt_content == 1 else 'JWT Token invalid.'
            })

        User.objects.get(pk=jwt_content.get('id'))
    except User.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'User not found.'
        })

    try:
        role = Role.objects.get(pk=role_id)
    except Role.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Role not found.'
        })

    data = role_normalizer(role)
    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': data})


@csrf_exempt
def add_role(request):
    if request.method != "POST":
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'error',
            'message': 'Must be a POST method',
        })

    try:
        authorization = request.headers.get('Authorization')
        jwt_content = tokenDecode.decode_token(authorization)
        if isinstance(jwt_content, int):
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
                'result': 'error',
                'message': 'An error has occurred while decoding the JWT Token.'
                if jwt_content == 1 else 'JWT Token invalid.'
            })

        user = User.objects.get(pk=jwt_content.get('id'))
    except User.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'User not found.'
        })

    if not (user.role == settings.ROLES['ROLE_ADMIN'] or user.role == settings.ROLES['ROLE_SUPER_ADMIN']):
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['FORBIDDEN'],
            'result': 'error',
            'message': 'You do not have the right privileges to access this resource.'
        })

    decode = request.body.decode('utf-8')
    content = json.loads(decode)
    form = RoleForm(content)

    if not form.is_valid():
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['INTERNAL_SERVER_ERROR'],
            'result': 'error',
            'message': 'Could not save the data',
            'data': form.errors
        })

    form.save()
    data = role_normalizer(Role.objects.latest('id'))
    return JsonResponse({'code': settings.HTTP_CONSTANTS['CREATED'], 'result': 'success', 'data': data})


@csrf_exempt
def update_role(request):
    if request.method != 'PATCH':
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'error',
            'message': 'Must be a PATCH method',
        })

    try:
        authorization = request.headers.get('Authorization')
        jwt_content = tokenDecode.decode_token(authorization)
        if isinstance(jwt_content, int):
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
                'result': 'error',
                'message': 'An error has occurred while decoding the JWT Token.'
                if jwt_content == 1 else 'JWT Token invalid.'
            })

        user = User.objects.get(pk=jwt_content.get('id'))
    except User.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'User not found.'
        })

    if not (user.role == settings.ROLES['ROLE_ADMIN'] or user.role == settings.ROLES['ROLE_SUPER_ADMIN']):
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['FORBIDDEN'],
            'result': 'error',
            'message': 'You do not have the right privileges to access this resource.'
        })

    decode = request.body.decode('utf-8')
    content = json.loads(decode)
    role_id = content['id']
    try:
        role = Role.objects.get(pk=role_id)
    except Role.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Role not found.'
        })

    form = RoleForm(instance=role, data=content)

    if not form.is_valid():
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Could not save the data',
            'data': form.errors
        })

    role.save()
    data = role_normalizer(role)
    return JsonResponse({'code': settings.HTTP_CONSTANTS['CREATED'], 'result': 'success', 'data': data})


@csrf_exempt
def delete_role(request, role_id):
    if request.method != 'DELETE':
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'error',
            'message': 'Must be a DELETE method',
        })

    try:
        authorization = request.headers.get('Authorization')
        jwt_content = tokenDecode.decode_token(authorization)
        if isinstance(jwt_content, int):
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
                'result': 'error',
                'message': 'An error has occurred while decoding the JWT Token.'
                if jwt_content == 1 else 'JWT Token invalid.'
            })

        user = User.objects.get(pk=jwt_content.get('id'))
    except User.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'User not found.'
        })

    if not (user.role == settings.ROLES['ROLE_ADMIN'] or user.role == settings.ROLES['ROLE_SUPER_ADMIN']):
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['FORBIDDEN'],
            'result': 'error',
            'message': 'You do not have the right privileges to access this resource.'
        })

    try:
        role = Role.objects.get(pk=role_id)
    except Role.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Role not found.'
        })

    role.delete()
    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': []})
