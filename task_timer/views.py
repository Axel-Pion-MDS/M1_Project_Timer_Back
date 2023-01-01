import django.middleware.csrf
import json

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from project.models import Project
from service import tokenDecode, verify_user_in_model, verify_user_role
from team.models import UserTeam
from user.models import User
from user_organization.models import UserOrganization
from .models import TaskTimer
from task.models import Task
from project.models import Project
from django.utils import timezone
from .normalizers import task_timer_normalizer, task_timers_normalizer
from .forms import TaskTimerForm

@csrf_exempt
def get_task_timers(request,task_id):

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
        project = Project.objects.get(pk=task.project.id)
    except Project.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Project not found.'
        })

    user_organization = verify_user_in_model.get_user_organization_from_project(user, project)
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
        user_team = verify_user_in_model.get_user_team_from_project(user, project)
        if not isinstance(user_team, UserTeam):
            return user_team

    try:
        task_timers = TaskTimer.objects.all().filter(task=task_id)
    except TaskTimer.DoesNotExist:
        return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': []})

    data = task_timers_normalizer(task_timers)
    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': data})

@csrf_exempt
def start_task_timer(request, task_id):
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

    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Task not found.'
        })

    try:
        project = Project.objects.get(pk=task.project.id)
    except Project.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Project not found.'
        })
    

    # Vérifie si l'utilisateur a accès à la tâche
    user_organization = verify_user_in_model.get_user_organization_from_project(user, project)
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
        user_team = verify_user_in_model.get_user_team_from_project(user, project)
        if not isinstance(user_team, UserTeam):
            return user_team

    task_timer = TaskTimer(start_time=timezone.now(),task=task)
    task_timer.save()
    return JsonResponse({
        'code': settings.HTTP_CONSTANTS['SUCCESS'],
        'result': 'success',
        'message': 'Task time successfully started'
        })


@csrf_exempt
def stop_task_timer(request, task_timer_id):
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

    try:
        task_timer = TaskTimer.objects.get(pk=task_timer_id)
    except TaskTimer.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'TaskTimer not found.'
        })

    try:
        task = Task.objects.get(id=task_timer.task.id)
    except Task.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Task not found.'
        })

    try:
        project = Project.objects.get(pk=task.project.id)
    except Project.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Project not found.'
        })

    user_organization = verify_user_in_model.get_user_organization_from_project(user, project)
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
        user_team = verify_user_in_model.get_user_team_from_project(user, project)
        if not isinstance(user_team, UserTeam):
            return user_team

    task_timer.end_time = timezone.now()
    duration = task_timer.end_time - task_timer.start_time
    task_timer.total_time = duration
    task_timer.save()
    return JsonResponse({
        'code': settings.HTTP_CONSTANTS['SUCCESS'],
        'result': 'success',
        'message': 'Task time successfully stoped'
    })
    

@csrf_exempt
def delete_task_timer(request, task_timer_id):
    if request.method != "DELETE":
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a DELETE method',
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
        task_timer = TaskTimer.objects.get(pk=task_timer_id)
    except TaskTimer.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'TaskTimer not found.'
        })

    try:
        task = Task.objects.get(id=task_timer.task.id)
    except Task.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Task not found.'
        })

    try:
        project = Project.objects.get(pk=task.project.id)
    except Project.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Project not found.'
        })

    user_organization = verify_user_in_model.get_user_organization_from_project(user, project)
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
        user_team = verify_user_in_model.get_user_team_from_project(user, project)
        if not isinstance(user_team, UserTeam):
            return user_team

    task_timer.delete()
    return JsonResponse({
        'code': settings.HTTP_CONSTANTS['SUCCESS'],
        'result': 'success',
        'message': 'Task time successfully deleted'
    })
    