import django.middleware.csrf
import json
import jwt

from django.conf import settings
from django.utils import timezone
from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import JsonResponse, HttpResponse


class TaskViewSet(viewsets.ModelViewSet):
  queryset = Task.objects.all()
  serializer_class = TaskSerializer

  @csrf_exempt
  def perform_create(self, serializer):
    serializer.save()
    return JsonResponse({'message': 'Successfully created task'}, status=201)

  @csrf_exempt
  def perform_update(self, serializer):
    serializer.save()
    return JsonResponse({'message': 'Task successfully updated'}, status=200)

  @csrf_exempt
  def perform_destroy(self, instance):
    instance.delete()
    return JsonResponse({'message': 'Task deleted successfully'}, status=204)

  @csrf_exempt
  def start(self, request, pk=None):
    if request.method == 'POST':

      task = self.get_object()
      if not task.start_time:
        task.start_time = timezone.now()
        task.save()
        return JsonResponse({'result': 'success','message': '',}, status=200)
      else:
        return JsonResponse({
          'code': 400,
          'result': 'error',
          'message': 'The task has already been launched',
        })

    else:
      return JsonResponse({
        'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
        'result': 'Not Allowed',
        'message': 'Must be a POST method',
      })

  @csrf_exempt
  def stop(self, request, pk=None):
    if request.method == 'POST':
      task = self.get_object()
      if task.start_time and not task.end_time:
        task.end_time = timezone.now()
        task.elapsed_time = task.end_time - task.start_time
        task.save()
      else:
        return JsonResponse({'result': 'error','message': 'The task has not yet been started or has already been stopped'}, status=400)
    else:
      return JsonResponse({
        'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
        'result': 'Not Allowed',
        'message': 'Must be a POST method',
      })

  @csrf_exempt
  def pause(self, request, pk=None):
    if request.method == 'POST':
      task = self.get_object()
      if task.start_time and not task.end_time and not task.paused:
        task.paused = True
        task.elapsed_time += timezone.now() - task.start_time
        task.save()
      elif task.paused:
        return JsonResponse({'result': 'error','message': 'The task is already paused'}, status=400)
      else:
        return JsonResponse({'result': 'error','message': 'The task has not yet been started or has already been stopped'}, status=400)
    else:
       return JsonResponse({
        'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
        'result': 'Not Allowed',
        'message': 'Must be a POST method',
      })

  @csrf_exempt
  def resume(self, request, pk=None):
    if request.method == 'POST':
      task = self.get_object()
      if task.start_time and not task.end_time and task.paused:
        task.paused = False
        task.start_time = timezone.now()
        task.save()
        return JsonResponse({'message': 'Successfully resumed task'}, status=200)
      elif not task.paused:
        return JsonResponse({'result': 'error','message': 'The task is not paused'}, status=400)
      else:
        return JsonResponse({'result': 'error','message': 'The task has not yet been started or has already been stopped'}, status=400)
    else:
       return JsonResponse({
        'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
        'result': 'Not Allowed',
        'message': 'Must be a POST method',
      })
      