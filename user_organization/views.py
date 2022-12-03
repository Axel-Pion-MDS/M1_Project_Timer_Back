import django.middleware.csrf
import json

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from organization.models import Organization
from role.models import Role
from service import tokenDecode
from user.models import User
from .models import UserOrganization
from .normalizers import user_organization_normalizer, user_organizations_normalizer, users_from_organization_normalizer
from .forms import UserOrganizationForm


@csrf_exempt
def get_user_organizations(request):
    if request.method == 'GET':
        user_organizations = UserOrganization.objects.all().values()

        if user_organizations:
            data = user_organizations_normalizer(user_organizations)
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
def get_user_organization(request, user_organization_id):
    if request.method == "GET":
        try:
            user_organization = UserOrganization.objects.get(pk=user_organization_id)
        except UserOrganization.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'User Organization not found.'
            })

        data = user_organization_normalizer(user_organization)
    else:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a GET method',
        })

    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': data})


@csrf_exempt
def get_users_from_organization(request, organization_id):
    if request.method == "GET":
        try:
            organization = Organization.objects.get(pk=organization_id)
        except Organization.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'Organization not found.'
            })

        try:
            user_organization = UserOrganization.objects.filter(organization=organization_id)
        except UserOrganization.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'User Organization not found.'
            })

        data = users_from_organization_normalizer(user_organization, organization)
    else:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a GET method',
        })

    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': data})


@csrf_exempt
def add_user_to_organization(request):
    if request.method == "POST":
        body = request.body.decode('utf-8')
        content = json.loads(body)
        form = UserOrganizationForm(content)

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
            organization = Organization.objects.get(pk=content['organization'])
        except Organization.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'Organization not found.'
            })

        try:
            user_organization = UserOrganization.objects.get(user=user, organization=organization)
            role_id = user_organization.role.id
            if not (role_id == settings.ROLES['ROLE_ORGANIZATION_OWNER'] or
                    role_id == settings.ROLES['ROLE_ORGANIZATION_CO_OWNER']):
                return JsonResponse({
                    'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
                    'result': 'error',
                    'message': 'You do not have the right privileges to access this resource.'
                })
        except UserOrganization.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'Organization not found for this User.'
            })

        try:
            user_to_add = User.objects.get(email=content['user'])
        except User.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'The User you are looking for has not been found.'
            })

        if user_to_add == user:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['FORBIDDEN'],
                'result': 'error',
                'message': 'Can not invite yourself.'
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
                'message': 'Wrong Role for Organization.'
            })

        content['user'] = user_to_add
        content['organization'] = organization
        content['role'] = role

        if form.is_valid():
            form.save()
            data = user_organization_normalizer(UserOrganization.objects.latest('id'))
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
def update_user_role_from_organization(request):
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
            organization = Organization.objects.get(pk=content['organization'])
        except Organization.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'Organization not found.'
            })

        try:
            user_organization = UserOrganization.objects.get(user=user, organization=organization)
            role_id = user_organization.role.id
            if not (role_id == settings.ROLES['ROLE_ORGANIZATION_OWNER'] or
                    role_id == settings.ROLES['ROLE_ORGANIZATION_CO_OWNER']):
                return JsonResponse({
                    'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
                    'result': 'error',
                    'message': 'You do not have the right privileges to access this resource.'
                })
        except UserOrganization.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'Organization not found for this User.'
            })

        try:
            user_to_update = User.objects.get(email=content['user'])
            try:
                organization_to_update = UserOrganization.objects.get(user=user_to_update, organization=organization)
            except UserOrganization.DoesNotExist:
                return JsonResponse({
                    'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                    'result': 'error',
                    'message': 'The User is not present in this Organization.'
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
                'message': 'Wrong Role for Organization.'
            })

        content['user'] = user_to_update
        content['organization'] = organization
        content['role'] = role

        form = UserOrganizationForm(instance=organization_to_update, data=content)

        if form.is_valid():
            organization_to_update.save()
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

    data = user_organization_normalizer(organization_to_update)

    return JsonResponse({'code': settings.HTTP_CONSTANTS['CREATED'], 'result': 'success', 'data': data})


@csrf_exempt
def delete_user_from_organization(request):
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
            organization = Organization.objects.get(pk=content['organization'])
        except Organization.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'Organization not found.'
            })

        try:
            user_organization = UserOrganization.objects.get(user=user, organization=organization)
            role_id = user_organization.role.id
            if not (role_id == settings.ROLES['ROLE_ORGANIZATION_OWNER'] or
                    role_id == settings.ROLES['ROLE_ORGANIZATION_CO_OWNER']):
                return JsonResponse({
                    'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
                    'result': 'error',
                    'message': 'You do not have the right privileges to access this resource.'
                })
        except UserOrganization.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'Organization not found for this User.'
            })

        try:
            user_to_delete = User.objects.get(email=content['user'])
            try:
                organization_to_update = UserOrganization.objects.get(user=user_to_delete, organization=organization)
            except UserOrganization.DoesNotExist:
                return JsonResponse({
                    'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                    'result': 'error',
                    'message': 'The User is not present in this Organization.'
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
                'message': 'You can not delete the owner, please delete the Organization instead.'
            })

        organization_to_update.delete()
    else:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a DELETE method',
        })

    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': []})

