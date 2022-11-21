import django.middleware.csrf
import json

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import User
from .normalizers import user_normalizer, users_normalizer
from .forms import UserForm


# @csrf_protect
@csrf_exempt
def add_user(request):
    if request.method == "POST":
        decode = request.body.decode('utf-8')
        content = json.loads(decode)
        form = UserForm(content)

        if form.is_valid():
            form.save()
            data = user_normalizer(User.objects.latest('id'))

            # if content['role']:
            #     try:
            #         santa = Role.objects.get(pk=content['role'])
            #     except Role.DoesNotExist:
            #         return JsonResponse({
            #             'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
            #             'result': 'error',
            #             'message': 'Role not found.'
            #         })
            #
            #     roleOrganization = RoleOrganization(organization=Organization.objects.latest('id'), role=role)
            #     RoleOrganization.save(roleOrganization)
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

