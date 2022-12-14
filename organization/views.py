import django.middleware.csrf
import json

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from user.models import User
from user_organization.forms import UserOrganizationForm
from user_organization.models import UserOrganization
from .models import Organization
from .normalizers import organization_normalizer, organizations_normalizer
from .forms import OrganizationForm
from service import tokenDecode


# @csrf_protect
@csrf_exempt
def get_organizations(request):
    if request.method != 'GET':
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'error',
            'message': 'Must be a GET method',
        })
    try:
        organizations = Organization.objects.all().values()
    except Organization.DoesNotExist:
        return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': []})

    data = organizations_normalizer(organizations)
    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': data})


@csrf_exempt
def get_organization(request, organization_id):
    if request.method != "GET":
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'error',
            'message': 'Must be a GET method',
        })

    try:
        organization = Organization.objects.get(pk=organization_id)
    except Organization.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Organization not found.'
        })

    data = organization_normalizer(organization)
    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': data})


@csrf_exempt
def add_organization(request):
    if request.method != "POST":
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'error',
            'message': 'Must be a POST method',
        })

    authorization = request.headers.get('Authorization')
    jwt_content = tokenDecode.decode_token(authorization)
    if isinstance(jwt_content, int):
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'error',
            'message': 'An error has occurred while decoding the JWT Token.'
            if jwt_content == 1 else 'JWT Token invalid.'
        })

    try:
        user = User.objects.get(pk=jwt_content.get('id'))
    except User.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'User not found.'
        })

    decode = request.body.decode('utf-8')
    content = json.loads(decode)
    organization_form = OrganizationForm(content)

    if not organization_form.is_valid():
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['INTERNAL_SERVER_ERROR'],
            'result': 'error',
            'message': 'Could not save the data in Organization',
            'data': organization_form.errors
        })

    organization_form.save()
    organization_data = Organization.objects.latest('id')

    user_organization = {
        'organization': organization_data.id,
        'user': user,
        'role': settings.ROLES['ROLE_ORGANIZATION_OWNER'],
    }

    user_organization_form = UserOrganizationForm(user_organization)
    if not user_organization_form.is_valid():
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['INTERNAL_SERVER_ERROR'],
            'result': 'error',
            'message': 'Could not save the data in User Organization',
            'data': user_organization_form.errors
        })

    user_organization_form.save()
    data = organization_normalizer(organization_data)
    return JsonResponse({'code': settings.HTTP_CONSTANTS['CREATED'], 'result': 'success', 'data': data})


@csrf_exempt
def update_organization(request):
    if request.method != 'PATCH':
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'error',
            'message': 'Must be a PATCH method',
        })

    authorization = request.headers.get('Authorization')
    jwt_content = tokenDecode.decode_token(authorization)
    if isinstance(jwt_content, int):
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'error',
            'message': 'An error has occurred while decoding the JWT Token.'
            if jwt_content == 1 else 'JWT Token invalid.'
        })

    try:
        user = User.objects.get(pk=jwt_content.get('id'))
    except User.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'User not found.'
        })

    decode = request.body.decode('utf-8')
    content = json.loads(decode)
    organization_id = content['organization']

    try:
        organization = Organization.objects.get(pk=organization_id)
    except Organization.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Organization not found.'
        })

    try:
        user_organization = UserOrganization.objects.get(user=user, organization=organization)
        if not (user_organization.role_id == settings.ROLES['ROLE_ORGANIZATION_OWNER'] or
                user_organization.role_id == settings.ROLES['ROLE_ORGANIZATION_CO_OWNER']):
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['FORBIDDEN'],
                'result': 'error',
                'message': 'You do not have the right privileges to access this resource.'
            })
    except UserOrganization.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'This user is not from this Organization.'
        })

    form = OrganizationForm(instance=organization, data=content)
    if not form.is_valid():
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Could not save the data',
            'data': form.errors
        })

    organization.save()
    data = organization_normalizer(organization)
    return JsonResponse({'code': settings.HTTP_CONSTANTS['CREATED'], 'result': 'success', 'data': data})


@csrf_exempt
def delete_organization(request, organization_id):
    if request.method != 'DELETE':
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'error',
            'message': 'Must be a DELETE method',
        })

    authorization = request.headers.get('Authorization')
    jwt_content = tokenDecode.decode_token(authorization)
    if isinstance(jwt_content, int):
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'error',
            'message': 'An error has occurred while decoding the JWT Token.'
            if jwt_content == 1 else 'JWT Token invalid.'
        })

    try:
        user = User.objects.get(pk=jwt_content.get('id'))
    except User.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'User not found.'
        })

    try:
        organization = Organization.objects.get(pk=organization_id)
    except Organization.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'Organization not found.'
        })

    try:
        user_organization = UserOrganization.objects.get(user=user, organization=organization)
        if user_organization.role_id != settings.ROLES['ROLE_ORGANIZATION_OWNER']:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
                'result': 'error',
                'message': 'You do not have the right privileges to access this resource.'
            })
    except UserOrganization.DoesNotExist:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            'result': 'error',
            'message': 'This user is not from this Organization.'
        })

    organization.delete()
    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': []})
