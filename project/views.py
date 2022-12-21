import django.middleware.csrf
import json
import jwt

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .normalizers import projects_normalizer, project_normalizer
from .forms import ProjectForm
from passlib.hash import pbkdf2_sha256
from environs import Env
from service import tokenDecode
from user.models import User
from .models import Project

env = Env()
env.read_env()
TOKEN_KEY = env("JWT_TOKEN_KEY")


# @csrf_protect

@csrf_exempt
def add_project(request):
    if request.method != "POST":
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a POST method',
        })
    try:
        authorization = request.headers.get('Authorization')
        jwt_content = tokenDecode.decode_token(authorization)
        User.objects.get(pk=jwt_content.get('id'))
    except User.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'User not found.'
        })
    if jwt_content.get('role').get('id') != settings.ROLES['ROLE_USER'] or settings.ROLES['ROLE_ORGANIZATION_CO_OWNER'] or settings.ROLES['ROLE_ORGANIZATION_TEAM_LEADER']:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'error',
            'message': "User doesn't have right access."
        })
    decode = request.body.decode('utf-8')
    content = json.loads(decode)

    label = content['label']
    if User.objects.filter(label=label).exists():
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'This user account already exists',
        })

    form = UserForm(content)
    if not form.is_valid():
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['INTERNAL_SERVER_ERROR'],
            'result': 'error',
            'message': 'Could not save the data',
            'data': form.errors
        })

    new_project = form.save(commit=False)
    new_project.save()
    data = user_normalizer(Project.objects.latest('id'))
    return JsonResponse({'code': settings.HTTP_CONSTANTS['CREATED'], 'result': 'success', 'project': data})


# @csrf_exempt
# def update_user(request):
#     if request.method != 'PATCH':
#         return JsonResponse({
#             'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
#             'result': 'Not Allowed',
#             'message': 'Must be a PATCH method',
#         })

#     decode = request.body.decode('utf-8')
#     content = json.loads(decode)
#     user_id = content['id']

#     try:
#         user = User.objects.get(pk=user_id)
#     except User.DoesNotExist:
#         return JsonResponse({
#             'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
#             'result': 'error',
#             'message': 'User not found.'
#         })

#     form = UserForm(instance=user, data=content)
#     if not form.is_valid():
#         return JsonResponse({
#             'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
#             'result': 'error',
#             'message': 'Could not save the data',
#             'data': form.errors
#         })

#     user_to_update = form.save(commit=False)
#     user_to_update.password = pbkdf2_sha256.hash(user_to_update.password)
#     user_to_update.save()
#     data = user_normalizer(user)
#     return JsonResponse({'code': settings.HTTP_CONSTANTS['CREATED'], 'result': 'success', 'data': data})


# @csrf_exempt
# def delete_user(request, user_id):
#     if request.method != 'DELETE':
#         return JsonResponse({
#             'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
#             'result': 'Not Allowed',
#             'message': 'Must be a DELETE method',
#         })

#     try:
#         user = User.objects.get(pk=user_id)
#     except User.DoesNotExist:
#         return JsonResponse({
#             'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
#             'result': 'error',
#             'message': 'User not found.'
#         })

#     user.delete()
#     return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': []})
