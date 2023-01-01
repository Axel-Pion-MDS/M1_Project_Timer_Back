import django.middleware.csrf
import json 

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from organization.models import Organization
from .normalizers import projects_normalizer, project_normalizer
from .forms import ProjectForm
from service import tokenDecode, verify_user_in_model
from user.models import User
from .models import Project
from user_organization.models import UserOrganization
from team.models import UserTeam

@csrf_exempt
def get_projects(request):
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
    if not (jwt_content.get('role').get('id') == settings.ROLES['ROLE_ADMIN'] or settings.ROLES['ROLE_SUPER_ADMIN']):
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['FORBIDDEN'],
            'result': 'error',
            'message': "User doesn't have right access."
        })

    projects = Project.objects.all().values()
    if not projects:
        return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': []})

    data = projects_normalizer(projects)
    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': data})


@csrf_exempt
def get_project(request, project_id):
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
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Project not found.'
        })

    data = project_normalizer(project)
    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': data})


# @csrf_protect
@csrf_exempt
def add_project(request):
    if request.method != "POST":
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'error',
            'message': 'Must be a POST method',
        })
    decode = request.body.decode('utf-8')
    content = json.loads(decode)
    organization = content["organization"]
    team = content['team'] if 'team' in content else None
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
        Organization.objects.get(pk=organization)
    except Organization.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Organization not found.'
        })

    try:
        user_organization = UserOrganization.objects.get(user=jwt_content.get('id'), organization=organization)
    except UserOrganization.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'User not found.'
        })

    if not (user_organization.role.id == settings.ROLES['ROLE_ORGANIZATION_OWNER'] or
            user_organization.role.id == settings.ROLES['ROLE_ORGANIZATION_CO_OWNER'] or
            user_organization.role.id == settings.ROLES['ROLE_ORGANIZATION_MEMBER']):
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['FORBIDDEN'],
            'result': 'error',
            'message': "User doesn't have right access."
        })
    if user_organization.role.id == settings.ROLES['ROLE_ORGANIZATION_MEMBER']:
        if team is None:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
                'result': 'error',
                'message': "User doesn't have right access."
            })
            
        try:
            user_team = UserTeam.objects.get(user=jwt_content.get('id'), team=team)
        except UserTeam.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'User not found.'
            })
        if not user_team.role.id == settings.ROLES['ROLE_TEAM_LEADER']:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['FORBIDDEN'],
                'result': 'error',
                'message': "User doesn't have right access."
            })

    label = content['label']
    if Project.objects.filter(label=label).exists():
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'error',
            'message': 'This project already exists',
        })

    form = ProjectForm(content)
    if not form.is_valid():
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['INTERNAL_SERVER_ERROR'],
            'result': 'error',
            'message': 'Could not save the data',
            'data': form.errors
        })

    new_project = form.save(commit=False)
    new_project.save()
    data = project_normalizer(Project.objects.latest('id'))
    return JsonResponse({'code': settings.HTTP_CONSTANTS['CREATED'], 'result': 'success', 'project': data})


@csrf_exempt
def update_project(request):
    if request.method != 'PATCH':
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'error',
            'message': 'Must be a PATCH method',
        })

    decode = request.body.decode('utf-8')
    content = json.loads(decode)
    project_id = content['id']
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
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'User not found.'
        })

    user_organization = verify_user_in_model.get_user_organization_from_project(user, project)
    if not isinstance(user_organization, UserOrganization):
        return user_organization

    if not (user_organization.role.id == settings.ROLES['ROLE_ORGANIZATION_OWNER'] or
            user_organization.role.id == settings.ROLES['ROLE_ORGANIZATION_CO_OWNER'] or
            user_organization.role.id == settings.ROLES['ROLE_ORGANIZATION_MEMBER']):

        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['FORBIDDEN'],
            'result': 'error',
            'message': "User doesn't have right access."
        })

    if user_organization.role.id == settings.ROLES['ROLE_ORGANIZATION_MEMBER']:
        user_team = verify_user_in_model.get_user_team_from_project(jwt_content.get('id'), project_id)
        if not isinstance(user_team, UserTeam):
            return user_team

        if not user_team.role.id == settings.ROLES['ROLE_TEAM_LEADER']:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['FORBIDDEN'],
                'result': 'error',
                'message': "User doesn't have right access."
            })

    form = ProjectForm(instance=project, data=content)
    if not form.is_valid():
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['INTERNAL_SERVER_ERROR'],
            'result': 'error',
            'message': 'Could not save the data',
            'data': form.errors
        })

    project_to_update = form.save(commit=False)
    project_to_update.save()
    data = project_normalizer(project_to_update)
    return JsonResponse({'code': settings.HTTP_CONSTANTS['CREATED'], 'result': 'success', 'data': data})


@csrf_exempt
def delete_project(request, project_id):
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

        User.objects.get(pk=jwt_content.get('id'))
    except User.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'User not found.'
        })

    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'User not found.'
        })

    user_organization = verify_user_in_model.get_user_organization_from_project(jwt_content.get('id'), project_id)
    if not isinstance(user_organization, UserOrganization):
        return user_organization

    if not (user_organization.role.id == settings.ROLES['ROLE_ORGANIZATION_OWNER'] or
            user_organization.role.id == settings.ROLES['ROLE_ORGANIZATION_CO_OWNER'] or
            user_organization.role.id == settings.ROLES['ROLE_ORGANIZATION_MEMBER']):
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['FORBIDDEN'],
            'result': 'error',
            'message': "User doesn't have right access."
        })

    if user_organization.role.id == settings.ROLES['ROLE_ORGANIZATION_MEMBER']:
        user_team = verify_user_in_model.get_user_team_from_project(jwt_content.get('id'), project_id)
        if not isinstance(user_team, UserTeam):
            return user_team

        if not user_team.role.id == settings.ROLES['ROLE_TEAM_LEADER']:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['FORBIDDEN'],
                'result': 'error',
                'message': "User doesn't have right access."
            })

    project.delete()
    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': []})
