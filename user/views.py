import django.middleware.csrf
import json
import jwt

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import User
from .normalizers import user_normalizer, users_normalizer
from .forms import UserForm, LoginForm
from passlib.hash import pbkdf2_sha256
from service import tokenDecode


# @csrf_protect
@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a POST method',
        })

    decode = request.body.decode('utf-8')
    content = json.loads(decode)

    email = content['email']
    password = content['password']
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'User not found.'
        })

    check_password = pbkdf2_sha256.verify(password, user.password)
    if not check_password:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'password incorrect',
        })

    login_form = LoginForm(content)
    if not login_form.is_valid():
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['INTERNAL_SERVER_ERROR'],
            'result': 'error',
            'message': 'Could not save the data',
            'data': login_form.errors
        })

    data = user_normalizer(user)
    jwt_body = {"id": user.id, "role": data["role"]}
    key = settings.TOKEN_KEY
    token = jwt.encode(jwt_body, key, algorithm="HS256")
    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'token': token, 'user': data})


@csrf_exempt
def get_users(request):
    if request.method != 'GET':
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a GET method',
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
    if not (jwt_content.get('role').get('id') == settings.ROLES['ROLE_ADMIN'] or settings.ROLES['ROLE_SUPER_ADMIN']):
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'error',
            'message': "User doesn't have right access."
        })

    users = User.objects.all().values()
    if not users:
        return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': []})

    data = users_normalizer(users)
    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': data})


@csrf_exempt
def get_user(request, user_id):
    if request.method != "GET":
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a GET method',
        })

    try:
        authorization = request.headers.get('Authorization')
        jwt_content = tokenDecode.decode_token(authorization)
        user = User.objects.get(pk=jwt_content.get('id'))
    except User.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'User not found.'
        })

    data = user_normalizer(user)
    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': data})


@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a POST method',
        })

    decode = request.body.decode('utf-8')
    content = json.loads(decode)

    email = content['email']
    if User.objects.filter(email=email).exists():
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

    new_user = form.save(commit=False)
    new_user.password = pbkdf2_sha256.hash(new_user.password)
    new_user.save()
    data = user_normalizer(User.objects.latest('id'))
    jwt_body = {"id": new_user.id, "role": data["role"]}
    key = settings.TOKEN_KEY
    token = jwt.encode(jwt_body, key, algorithm="HS256")
    return JsonResponse({'code': settings.HTTP_CONSTANTS['CREATED'], 'result': 'success', 'token': token, 'user': data})


@csrf_exempt
def update_user(request):
    if request.method != 'PATCH':
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a PATCH method',
        })

    decode = request.body.decode('utf-8')
    content = json.loads(decode)
    id = content["id"]

    try:
        authorization = request.headers.get('Authorization')
        jwt_content = tokenDecode.decode_token(authorization)
        user = User.objects.get(pk=jwt_content.get('id'))
    except User.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'User not found.'
        })
    if id != user.id:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['FORBIDDEN'],
            'result': 'error',
            'message': 'User can only update your own profile'
        })
    form = UserForm(instance=user, data=content)
    if not form.is_valid():
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Could not save the data',
            'data': form.errors
        })

    user_to_update = form.save(commit=False)
    user_to_update.password = pbkdf2_sha256.hash(user_to_update.password)
    user_to_update.save()
    data = user_normalizer(user)
    return JsonResponse({'code': settings.HTTP_CONSTANTS['CREATED'], 'result': 'success', 'data': data})


@csrf_exempt
def update_user(request, user_id):
    if request.method == 'PATCH':
        decode = request.body.decode('utf-8')
        content = json.loads(decode)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'User not found.'
            })

        form = UserForm(instance=user, data=content)

        if form.is_valid():
            update_user = form.save(commit=False)
            update_user.password = pbkdf2_sha256.hash(update_user.password)
            update_user.save()
        else:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'Could not save the data',
                'data': form.errors
            })

    else:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a PATCH method',
        })

    data = user_normalizer(user)

    return JsonResponse({'code': settings.HTTP_CONSTANTS['CREATED'], 'result': 'success', 'data': data})


@csrf_exempt
def delete_user(request, user_id):
    if request.method != 'DELETE':
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a DELETE method',
        })

    try:
        authorization = request.headers.get('Authorization')
        jwt_content = tokenDecode.decode_token(authorization)
        user = User.objects.get(pk=jwt_content.get('id'))
    except User.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'User not found.'
        })
    if user_id != user.id:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['FORBIDDEN'],
            'result': 'error',
            'message': 'User can only update your own profile'
        })

    user.delete()
    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': []})
