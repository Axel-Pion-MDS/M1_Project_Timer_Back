from django.http import JsonResponse

from app import settings
from organization.models import Organization
from team.models import Team, UserTeam
from user_organization.models import UserOrganization


def get_user_organization_from_project(user, project_id):
    organization = get_project_from_organization(project_id)
    try:
        user_organization = UserOrganization.objects.get(user=user.id, organization=organization.id)
    except UserOrganization.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'UserOrganization not found.'
        })

    return user_organization


def get_user_team_from_project(user, project_id):
    team = get_project_from_team(project_id)
    try:
        user_team = UserTeam.objects.get(user=user.id, team=team.id)
    except UserTeam.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'UserTeam not found for this organization\'s member.'
        })

    return user_team


def get_project_from_organization(project_id):
    try:
        organization = Organization.objects.get(project=project_id)
    except Organization.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Organization not found.'
        })

    return organization


def get_project_from_team(project_id):
    try:
        team = Team.objects.get(project=project_id)
    except Team.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Team not found.'
        })

    return team


def get_team_from_project(project_id):
    try:
        team = Team.objects.get(project=project_id)
    except Team.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Team not found.'
        })
