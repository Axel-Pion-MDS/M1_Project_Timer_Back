from django.http import JsonResponse

from app import settings
from organization.models import Organization
from project.models import Project
from team.models import Team, UserTeam
from user_organization.models import UserOrganization


def get_user_organization_from_project(user, project):
    organization = get_organization_from_project(project)

    try:
        user_organization = UserOrganization.objects.get(user=user, organization=organization)
    except UserOrganization.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'UserOrganization not found.'
        })

    return user_organization


def get_user_team_from_project(user, project):
    team = get_team_from_project(project)
    try:
        user_team = UserTeam.objects.get(user=user.id, team=team.id)
    except UserTeam.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'UserTeam not found for this organization\'s member.'
        })

    return user_team


def get_organization_from_project(project):
    try:
        project = Project.objects.get(pk=project.id)
    except Project.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Project not found.'
        })

    return project.organization.id


def get_team_from_project(project):
    try:
        project = Project.objects.get(pk=project.id)
    except Project.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Project not found.'
        })

    return project.team.id if project.team.id else JsonResponse({
        'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
        'result': 'error',
        'message': 'This Project has no Team.'
    })
