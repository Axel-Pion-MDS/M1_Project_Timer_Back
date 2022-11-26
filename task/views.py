import django.middleware.csrf
import json

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import Task
from .normalizers import task_normalizer, tasks_normalizer
from .forms import TaskForm


# @csrf_protect
@csrf_exempt
def get_tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.all().values()

        if tasks:
            data = tasks_normalizer(tasks)
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
def get_task(request, task_id):
    if request.method == "GET":
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'Task not found.'
            })

        data = task_normalizer(task)
    else:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a GET method',
        })

    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': data})


@csrf_exempt
def add_task(request):
    if request.method == "POST":
        decode = request.body.decode('utf-8')
        content = json.loads(decode)
        form = TaskForm(content)

        if form.is_valid():
            form.save()
            data = task_normalizer(Task.objects.latest('id'))
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
def update_task(request):
    if request.method == 'PATCH':
        decode = request.body.decode('utf-8')
        content = json.loads(decode)
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

        if form.is_valid():
            task.save()
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

    data = task_normalizer(task)

    return JsonResponse({'code': settings.HTTP_CONSTANTS['CREATED'], 'result': 'success', 'data': data})


@csrf_exempt
def delete_task(request, task_id):
    if request.method == 'DELETE':
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return JsonResponse({
                'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
                'result': 'error',
                'message': 'Task not found.'
            })

        task.delete()
    else:
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a DELETE method',
        })

    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': []})