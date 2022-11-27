import django.middleware.csrf
import json

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import Organization
from .normalizers import organization_normalizer, organizations_normalizer
from .forms import OrganizationForm


# @csrf_protect
@csrf_exempt
def get_organizations(request):
    if request.method == 'GET':
        organizations = Organization.objects.all().values()

        if organizations:
            data = organizations_normalizer(organizations)
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
def get_organization(request, organization_id):
    if request.method == "GET":
        try:
            organization = Organization.objects.get(pk=organization_id)
        except Organization.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'Organization not found.'
            })

        data = organization_normalizer(organization)
    else:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a GET method',
        })

    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': data})


@csrf_exempt
def add_organization(request):
    if request.method == "POST":
        decode = request.body.decode('utf-8')
        content = json.loads(decode)
        organization_form = OrganizationForm(content)

        if organization_form.is_valid():
            organization_form.save()
            organization_data = Organization.objects.latest('id')
            organization_id = organization_data.id
            current_user = request.user
            role = settings.ROLES['ROLE_ORGANIZATION_OWNER']   
            
            user_organization_form = UserOrganizationForm(organization_id, current_user, role)
            
            if user_organization_form.is_valid():
                user_organization_form.save()
                data = organization_normalizer(organization_data)
            else:
                return JsonResponse({
                    'code': settings.HTTP_CONSTANTS['INTERNAL_SERVER_ERROR'],
                    'result': 'error',
                    'message': 'Could not save the data in User Organization',
                    'data': user_organization_form.errors
                })
        else:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['INTERNAL_SERVER_ERROR'],
                'result': 'error',
                'message': 'Could not save the data in Organization',
                'data': organization_form.errors
            })
    else:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a POST method',
        })

    return JsonResponse({'code': settings.HTTP_CONSTANTS['CREATED'], 'result': 'success', 'data': data})


@csrf_exempt
def update_organization(request):
    if request.method == 'PATCH':
        decode = request.body.decode('utf-8')
        content = json.loads(decode)
        organization_id = content['id']

        try:
            organization = Organization.objects.get(pk=organization_id)
        except Organization.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'Organization not found.'
            })

        form = OrganizationForm(instance=organization, data=content)

        if form.is_valid():
            organization.save()
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

    data = organization_normalizer(organization)

    return JsonResponse({'code': settings.HTTP_CONSTANTS['CREATED'], 'result': 'success', 'data': data})


@csrf_exempt
def delete_organization(request, organization_id):
    if request.method == 'DELETE':
        try:
            organization = Organization.objects.get(pk=organization_id)
        except Organization.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'Organization not found.'
            })

        organization.delete()
    else:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a DELETE method',
        })

    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': []})
