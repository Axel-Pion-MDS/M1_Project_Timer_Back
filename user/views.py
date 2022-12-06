import django.middleware.csrf
import json

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import User
from .normalizers import user_normalizer, users_normalizer
from .forms import UserForm, LoginForm
from passlib.hash import pbkdf2_sha256


# @csrf_protect
@csrf_exempt
def login(request):
    if request.method == 'POST':
        decode = request.body.decode('utf-8')
        content = json.loads(decode)
        login_form = LoginForm(content)
        if login_form.is_valid():
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
            if check_password:
                message = 'You are logged in'
            else:
                return JsonResponse({
                    'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
                    'result': 'Not Allowed',
                    'message': 'password incorrect',
                })
        else:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['INTERNAL_SERVER_ERROR'],
                'result': 'error',
                'message': 'Could not save the data',
                'data': login_form.errors
            })
    else:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a POST method',
        })
    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'message': message})


@csrf_exempt
def get_users(request):
    if request.method == 'GET':
        users = User.objects.all().values()
        if users:
            data = users_normalizer(users)
        else:
            return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': []})
    else:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a GET method',
        })

    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': data})


@csrf_exempt
def get_user(request, user_id):
    if request.method == "GET":
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'User not found.'
            })

        data = user_normalizer(user)
    else:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a GET method',
        })

    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': data})


@csrf_exempt
def register(request):
    if request.method == "POST":
        decode = request.body.decode('utf-8')
        content = json.loads(decode)
        form = UserForm(content)

        if form.is_valid():
            email = content['email']
            if not User.objects.filter(email=email).exists():
                new_user = form.save(commit=False)
                new_user.password = pbkdf2_sha256.hash(new_user.password)
                new_user.save()
                data = user_normalizer(User.objects.latest('id'))
            else:
                return JsonResponse({
                    'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
                    'result': 'Not Allowed',
                    'message': 'This user account already exists',
                })      
        else:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['INTERNAL_SERVER_ERROR'],
                'result': 'error',
                'message': 'Could not save the data',
                'data': form.errors
            })
    else:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a POST method',
        })

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
    if request.method == 'DELETE':
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'User not found.'
            })

        user.delete()
    else:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a DELETE method',
        })

    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': []})
