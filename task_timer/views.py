import django.middleware.csrf
import json
import jwt

from django.conf import settings
from django.utils import timezone
from rest_framework import viewsets
from .models import TaskTimer
from .serializers import TaskTimerSerializer
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import JsonResponse, HttpResponse


class TaskTimerViewSet(viewsets.ModelViewSet):
  queryset = TaskTimer.objects.all()
  serializer_class = TaskTimerSerializer

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
      task_timer = self.get_object()
      task_timer.start_time = timezone.now()
      task_timer.save()
      return JsonResponse({'message': 'Task time successfully started'}, status=200)
    else:
      return JsonResponse({
        'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
        'result': 'Not Allowed',
        'message': 'Must be a POST method',
      })

  @csrf_exempt
  def stop(self, request, pk=None):
    if request.method == 'POST':
      task_timer = self.get_object()
      task_timer.end_time = timezone.now()
      duration = task_timer.end_time - task_timer.start_time
      task_timer.total_time = duration
      task_timer.save()
      return JsonResponse({'message': 'Successfully stopped task time'}, status=200)
    else:
      return JsonResponse({
        'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
        'result': 'Not Allowed',
        'message': 'Must be a POST method',
      })

  @csrf_exempt
  def pause(self, request, pk=None):
    if request.method == 'POST':
      task_timer = self.get_object()
      duration = timezone.now() - task_timer.start_time
      task_timer.total_time += duration
      task_timer.save()
      return JsonResponse({'message': 'Successfully paused task time'}, status=200)
    else:
       return JsonResponse({
        'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
        'result': 'Not Allowed',
        'message': 'Must be a POST method',
      })

  @csrf_exempt
  def resume(self, request, pk=None):
    if request.method == 'POST':
      task_timer = self.get_object()
      task_timer.start_time = timezone.now()
      task_timer.save()
      return JsonResponse({'message': 'Temps de tâche repris avec succès'}, status=200)
    else:
       return JsonResponse({
        'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
        'result': 'Not Allowed',
        'message': 'Must be a POST method',
      })
      