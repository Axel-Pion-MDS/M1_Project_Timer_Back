import django.middleware.csrf
import json

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import UserOrganization
from .normalizers import user_organization_normalizer, user_organizations_normalizer
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
def add_user_organization(request):
    if request.method == "POST":
        decode = request.body.decode('utf-8')
        content = json.loads(decode)
        form = UserOrganizationForm(content)

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
def update_user_organization(request):
    if request.method == 'PATCH':
        decode = request.body.decode('utf-8')
        content = json.loads(decode)
        user_organization_id = content['id']

        try:
            user_organization = UserOrganization.objects.get(pk=user_organization_id)
        except UserOrganization.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'User Organization not found.'
            })

        form = UserOrganizationForm(instance=user_organization, data=content)

        if form.is_valid():
            user_organization.save()
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

    data = user_organization_normalizer(user_organization)

    return JsonResponse({'code': settings.HTTP_CONSTANTS['CREATED'], 'result': 'success', 'data': data})


@csrf_exempt
def delete_user_organization(request, user_organization_id):
    if request.method == 'DELETE':
        try:
            user_organization = UserOrganization.objects.get(pk=user_organization_id)
        except UserOrganization.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'User Organization not found.'
            })

        user_organization.delete()
    else:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a DELETE method',
        })

    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': []})

