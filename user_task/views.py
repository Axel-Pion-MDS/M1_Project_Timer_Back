import django.middleware.csrf
import json

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from task.models import Task
from role.models import Role
from service import tokenDecode
from team.models import UserTeam
from user.models import User
from user_organization.models import UserOrganization
from .models import UserTask
from .normalizers import user_task_normalizer, user_tasks_normalizer, users_from_task_normalizer
from .forms import UserTaskForm


@csrf_exempt
def get_user_tasks(request):
    if request.method != 'GET':
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a GET method',
        })

    try:
        authorization = request.headers.get('Authorization')
        jwt_content = tokenDecode.decode_token(authorization)
        user = User.objects.get(id=jwt_content.get('id'))
    except User.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'User not found.'
        })

    try:
        user_tasks = UserTask.objects.all().get(user=user.id)
    except UserTask.DoesNotExist:
        return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': []})

    data = user_tasks_normalizer(user_tasks)
    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': data})


@csrf_exempt
def get_user_task(request, user_task_id):
    if request.method != "GET":
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a GET method',
        })

    try:
        authorization = request.headers.get('Authorization')
        jwt_content = tokenDecode.decode_token(authorization)
        User.objects.get(id=jwt_content.get('id'))
    except User.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'User not found.'
        })

    try:
        user_task = UserTask.objects.get(pk=user_task_id)
    except UserTask.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'User Task not found.'
        })

    data = user_task_normalizer(user_task)
    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': data})


@csrf_exempt
def get_users_from_task(request, task_id):
    if request.method != "GET":
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a GET method',
        })

    try:
        authorization = request.headers.get('Authorization')
        jwt_content = tokenDecode.decode_token(authorization)
        user = User.objects.get(id=jwt_content.get('id'))
    except User.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'User not found.'
        })

    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Task not found.'
        })

    try:
        user_task = UserTask.objects.filter(task=task_id)
    except UserTask.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'User Task not found.'
        })

    data = users_from_task_normalizer(user_task, task)
    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': data})


@csrf_exempt
def add_user_to_task(request):
    if request.method != "POST":
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a POST method',
        })
    body = request.body.decode('utf-8')
    content = json.loads(body)
    form = UserTaskForm(content)

    try:
        authorization = request.headers.get('Authorization')
        jwt_content = tokenDecode.decode_token(authorization)
        user = User.objects.get(id=jwt_content.get('id'))
    except User.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'User not found.'
        })

    try:
        user_organization = UserOrganization.objects.get(pk=user.id)
    except UserOrganization.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'This user is not in the organization.'
        })

    role_id = user_organization.role_id
    if not (role_id == settings.ROLES['ROLE_ORGANIZATION_OWNER'] or
            role_id == settings.ROLES['ROLE_ORGANIZATION_CO_OWNER']):
        try:
            user_team = UserTeam.objects.get(pk=user.id)
        except UserTeam.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
                'result': 'error',
                'message': 'You do not have the right privileges to access this resource.'
            })

        if not (user_team.role_id == settings.ROLES['ROLE_TEAM_LEADER']):
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
                'result': 'error',
                'message': 'You do not have the right privileges to access this resource.'
            })

    try:
        task = Task.objects.get(pk=content['task'])
    except Task.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Task not found.'
        })

    try:
        user_to_add = User.objects.get(email=content['user'])
    except User.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'The User you are looking for has not been found.'
        })

    try:
        UserOrganization.objects.get(pk=user_to_add.id)
        UserTeam.objects.get(pk=user_to_add.id)
    except UserOrganization.DoesNotExist or UserTeam.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'The User you are looking for is not a member of that organization or team.'
        })

    content['user'] = user_to_add
    content['task'] = task

    if not form.is_valid():
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['INTERNAL_SERVER_ERROR'],
            'result': 'error',
            'message': 'Could not save the data',
            'data': form.errors
        })

    form.save()
    data = user_task_normalizer(UserTask.objects.latest('id'))

    return JsonResponse({'code': settings.HTTP_CONSTANTS['CREATED'], 'result': 'success', 'data': data})


@csrf_exempt
def update_user_role_from_task(request):
    if request.method == 'PATCH':
        body = request.body.decode('utf-8')
        content = json.loads(body)

        try:
            authorization = request.headers.get('Authorization')
            jwt_content = tokenDecode.decode_token(authorization)
            user = User.objects.get(id=jwt_content.get('id'))
        except User.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'User not found.'
            })

        try:
            task = Task.objects.get(pk=content['task'])
        except Task.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'Task not found.'
            })

        try:
            user_task = UserTask.objects.get(user=user, task=task)
            role_id = user_task.role.id
            if not (role_id == settings.ROLES['ROLE_ORGANIZATION_OWNER'] or
                    role_id == settings.ROLES['ROLE_ORGANIZATION_CO_OWNER']):
                return JsonResponse({
                    'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
                    'result': 'error',
                    'message': 'You do not have the right privileges to access this resource.'
                })
        except UserTask.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'Task not found for this User.'
            })

        try:
            user_to_update = User.objects.get(email=content['user'])
            try:
                task_to_update = UserTask.objects.get(user=user_to_update, task=task)
            except UserTask.DoesNotExist:
                return JsonResponse({
                    'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                    'result': 'error',
                    'message': 'The User is not present in this Task.'
                })
        except User.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'The User you are looking for has not been found.'
            })

        if user_to_update == user:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['FORBIDDEN'],
                'result': 'error',
                'message': 'Can not update yourself.'
            })

        try:
            role = Role.objects.get(pk=content['role'])
        except Role.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'Role not found.'
            })

        if not (role.id == settings.ROLES['ROLE_ORGANIZATION_CO_OWNER'] or
                role.id == settings.ROLES['ROLE_ORGANIZATION_MEMBER']):
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['FORBIDDEN'],
                'result': 'error',
                'message': 'Wrong Role for Task.'
            })

        content['user'] = user_to_update
        content['task'] = task
        content['role'] = role

        form = UserTaskForm(instance=task_to_update, data=content)

        if form.is_valid():
            task_to_update.save()
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

    data = user_task_normalizer(task_to_update)

    return JsonResponse({'code': settings.HTTP_CONSTANTS['CREATED'], 'result': 'success', 'data': data})


@csrf_exempt
def delete_user_from_task(request):
    if request.method == 'DELETE':
        body = request.body.decode('utf-8')
        content = json.loads(body)

        try:
            authorization = request.headers.get('Authorization')
            jwt_content = tokenDecode.decode_token(authorization)
            user = User.objects.get(id=jwt_content.get('id'))
        except User.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'User not found.'
            })

        try:
            task = Task.objects.get(pk=content['task'])
        except Task.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'Task not found.'
            })

        try:
            user_task = UserTask.objects.get(user=user, task=task)
            role_id = user_task.role.id
            if not (role_id == settings.ROLES['ROLE_ORGANIZATION_OWNER'] or
                    role_id == settings.ROLES['ROLE_ORGANIZATION_CO_OWNER']):
                return JsonResponse({
                    'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
                    'result': 'error',
                    'message': 'You do not have the right privileges to access this resource.'
                })
        except UserTask.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'Task not found for this User.'
            })

        try:
            user_to_delete = User.objects.get(email=content['user'])
            try:
                task_to_update = UserTask.objects.get(user=user_to_delete, task=task)
            except UserTask.DoesNotExist:
                return JsonResponse({
                    'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                    'result': 'error',
                    'message': 'The User is not present in this Task.'
                })
        except User.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'The User you are looking for has not been found.'
            })

        if user_to_delete == user:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['FORBIDDEN'],
                'result': 'error',
                'message': 'Can not delete yourself.'
            })

        if ((user_to_delete.role.id == settings.ROLES['ROLE_ORGANIZATION_CO_OWNER'] or
             user_to_delete.role.id == settings.ROLES['ROLE_ORGANIZATION_MEMBER']) and
                user.role.id != settings.ROLES['ROLE_ORGANIZATION_OWNER']):
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
                'result': 'error',
                'message': 'You do not have the right privileges to access this resource.'
            })

        if (user_to_delete.role.id == settings.ROLES['ROLE_ORGANIZATION_MEMBER'] and
                user.role.id != settings.ROLES['ROLE_ORGANIZATION_OWNER']):
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
                'result': 'error',
                'message': 'You do not have the right privileges to access this resource.'
            })

        if (user_to_delete.role.id == settings.ROLES['ROLE_ORGANIZATION_OWNER'] and
                user.role.id == settings.ROLES['ROLE_ORGANIZATION_OWNER']):
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['FORBIDDEN'],
                'result': 'error',
                'message': 'You can not delete the owner, please delete the Task instead.'
            })

        task_to_update.delete()
    else:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a DELETE method',
        })

    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': []})
