import django.middleware.csrf
import json

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from service import tokenDecode, verify_user_in_model, verify_user_role
from team.models import Team, UserTeam
from user.models import User
from user_organization.models import UserOrganization
from .models import Task
from .normalizers import task_normalizer, tasks_normalizer
from .forms import TaskForm


def get_tasks(request, project_id):
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
        Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Project not found.'
        })

    user_organization = verify_user_in_model.get_user_organization_from_project(user, project_id)
    if not isinstance(user_organization, UserOrganization):
        return user_organization

    role_id = user_organization.role_id
    has_role = verify_user_role.has_role(
        role_id,
        [
            'ROLE_ORGANIZATION_OWNER',
            'ROLE_ORGANIZATION_CO_OWNER',
            'ROLE_ORGANIZATION_MEMBER'
        ],
        'You are not a member of this organization.'
    )

    if not has_role:
        return has_role

    if role_id == settings.ROLES['ROLE_ORGANIZATION_MEMBER']:
        user_team = verify_user_in_model.get_user_team_from_project(user, project_id)
        if not isinstance(user_team, UserTeam):
            return user_team

    tasks = Task.objects.all()
    data = tasks_normalizer(tasks)
    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': data})


@csrf_exempt
def get_task(request, task_id):
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

    project_id = task.project.id
    try:
        Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Project not found.'
        })

    user_organization = verify_user_in_model.get_user_organization_from_project(user, project_id)
    if not isinstance(user_organization, UserOrganization):
        return user_organization

    role_id = user_organization.role_id
    has_role = verify_user_role.has_role(
        role_id,
        [
            'ROLE_ORGANIZATION_OWNER',
            'ROLE_ORGANIZATION_CO_OWNER',
            'ROLE_ORGANIZATION_MEMBER'
        ],
        'You are not a member of this organization.'
    )
    if not has_role:
        return has_role

    if role_id == settings.ROLES['ROLE_ORGANIZATION_MEMBER']:
        user_team = verify_user_in_model.get_user_team_from_project(user, project_id)
        if not isinstance(user_team, UserTeam):
            return user_team

    data = task_normalizer(task)
    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': data})


@csrf_exempt
def add_task(request):
    if request.method != "POST":
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a POST method',
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

    decode = request.body.decode('utf-8')
    content = json.loads(decode)

    try:
        project = Project.objects.get(pk=content['project'])
    except Project.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Project not found.'
        })

    user_organization = verify_user_in_model.get_user_organization_from_project(user, project.id)
    if not isinstance(user_organization, UserOrganization):
        return user_organization

    role_id = user_organization.role_id
    has_role = verify_user_role.has_role(
        role_id,
        [
            'ROLE_ORGANIZATION_OWNER',
            'ROLE_ORGANIZATION_CO_OWNER',
            'ROLE_ORGANIZATION_MEMBER'
        ],
        'You are not a member of this organization.'
    )

    if not has_role:
        return has_role

    if role_id == settings.ROLES['ROLE_ORGANIZATION_MEMBER']:
        user_team = verify_user_in_model.get_user_team_from_project(user, project.id)
        if not isinstance(user_team, UserTeam):
            return user_team

        role_id = user_team.role_id
        has_role = verify_user_role.has_role(role_id, ['ROLE_TEAM_LEADER'])

        if not has_role:
            return has_role

    form = TaskForm(content)
    if not form.is_valid():
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['INTERNAL_SERVER_ERROR'],
            'result': 'error',
            'message': 'Could not save the data',
            'data': form.errors
        })

    form.save()
    data = task_normalizer(Task.objects.latest('id'))
    return JsonResponse({'code': settings.HTTP_CONSTANTS['CREATED'], 'result': 'success', 'data': data})


@csrf_exempt
def update_task(request):
    if request.method != 'PATCH':
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a PATCH method',
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

    decode = request.body.decode('utf-8')
    content = json.loads(decode)

    try:
        project = Project.objects.get(pk=content['project'])
    except Project.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Project not found.'
        })

    user_organization = verify_user_in_model.get_user_organization_from_project(user, project.id)
    if not isinstance(user_organization, UserOrganization):
        return user_organization

    role_id = user_organization.role_id
    has_role = verify_user_role.has_role(
        role_id,
        [
            'ROLE_ORGANIZATION_OWNER',
            'ROLE_ORGANIZATION_CO_OWNER',
            'ROLE_ORGANIZATION_MEMBER'
        ],
        'You are not a member of this organization.'
    )

    if not has_role:
        return has_role

    if role_id == settings.ROLES['ROLE_ORGANIZATION_MEMBER']:
        user_team = verify_user_in_model.get_user_team_from_project(user, project.id)
        if not isinstance(user_team, UserTeam):
            return user_team

        role_id = user_team.role_id
        has_role = verify_user_role.has_role(role_id, ['ROLE_TEAM_LEADER'])

        if not has_role:
            return has_role

    task_id = content['id']
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Task not found.'
        })

    form = TaskForm(instance=task, data=content)
    if not form.is_valid():
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Could not save the data',
            'data': form.errors
        })

    task.save()
    data = task_normalizer(task)
    return JsonResponse({'code': settings.HTTP_CONSTANTS['CREATED'], 'result': 'success', 'data': data})


@csrf_exempt
def delete_task(request, task_id):
    if request.method != 'DELETE':
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a DELETE method',
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
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Task not found.'
        })
    
    try:
        project = Project.objects.get(pk=task.project_id)
    except Project.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Project not found.'
        })

    user_organization = verify_user_in_model.get_user_organization_from_project(user, project.id)
    if not isinstance(user_organization, UserOrganization):
        return user_organization

    role_id = user_organization.role_id
    has_role = verify_user_role.has_role(
        role_id,
        [
            'ROLE_ORGANIZATION_OWNER',
            'ROLE_ORGANIZATION_CO_OWNER',
            'ROLE_ORGANIZATION_MEMBER'
        ],
        'You are not a member of this organization.'
    )

    if not has_role:
        return has_role

    if role_id == settings.ROLES['ROLE_ORGANIZATION_MEMBER']:
        user_team = verify_user_in_model.get_user_team_from_project(user, project.id)
        if not isinstance(user_team, UserTeam):
            return user_team

        role_id = user_team.role_id
        has_role = verify_user_role.has_role(role_id, ['ROLE_TEAM_LEADER'])

        if not has_role:
            return has_role

    task.delete()
    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': []})
