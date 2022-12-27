import django.middleware.csrf
import json

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from project.models import Project
from service import tokenDecode, verify_user_in_model
from team.models import UserTeam
from user.models import User
from user_organization.models import UserOrganization
from .models import TaskTimer
# from .models import Task
from .normalizers import task_timer_normalizer, task_timers_normalizer
# from .forms import TaskTimerForm

@csrf_exempt
def get_task_timers(request, task_id):
    if request.method != "GET":
        return JsonResponse({
            'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
            'result': 'Not Allowed',
            'message': 'Must be a GET method',
        })

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

    # try:
    #     task = Task.objects.get(pk=task_id)
    # except Task.DoesNotExist:
    #     return JsonResponse({
    #         'code': settings.HTTP_CONSTANTS['NOT_FOUND'],
    #         'result': 'error',
    #         'message': 'Task not found.'
    #     })

    # user_organization = verify_user_in_model.get_user_organization_from_project(user, task.project)
    # if not isinstance(user_organization, UserOrganization):
    #     return user_organization

    # role_id = user_organization.role_id
    # has_role = verify_user_role.has_role(
    #     role_id,
    #     [
    #         'ROLE_ORGANIZATION_OWNER',
    #         'ROLE_ORGANIZATION_CO_OWNER',
    #         'ROLE_ORGANIZATION_MEMBER'
    #     ],
    #     'You are not a member of this organization.'
    # )

    # if not has_role:
    #     return has_role

    # if role_id == settings.ROLES['ROLE_ORGANIZATION_MEMBER']:
    #     user_team = verify_user_in_model.get_user_team_from_project(user, task.project)
    #     if not isinstance(user_team, UserTeam):
    #         return user_team

    try:
        task_timers = TaskTimer.objects.all().filter(task=task_id)
    except TaskTimer.DoesNotExist:
        return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': []})

    data = task_timers_normalizer(task_timers)
    return JsonResponse({'code': settings.HTTP_CONSTANTS['SUCCESS'], 'result': 'success', 'data': data})

# class TaskTimerViewSet(viewsets.ModelViewSet):
#   queryset = TaskTimer.objects.all()
#   serializer_class = TaskTimerSerializer

#   @csrf_exempt
#   def perform_create(self, serializer):
#     serializer.save()
#     return JsonResponse({'message': 'Successfully created task'}, status=201)

#   @csrf_exempt
#   def perform_update(self, serializer):
#     serializer.save()
#     return JsonResponse({'message': 'Task successfully updated'}, status=200)

#   @csrf_exempt
#   def perform_destroy(self, instance):
#     instance.delete()
#     return JsonResponse({'message': 'Task deleted successfully'}, status=204)

#   @csrf_exempt
#   def start(self, request, pk=None):
#     if request.method == 'POST':
#       task_timer = self.get_object()
#       task_timer.start_time = timezone.now()
#       task_timer.save()
#       return JsonResponse({'message': 'Task time successfully started'}, status=200)
#     else:
#       return JsonResponse({
#         'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
#         'result': 'Not Allowed',
#         'message': 'Must be a POST method',
#       })

#   @csrf_exempt
#   def stop(self, request, pk=None):
#     if request.method == 'POST':
#       task_timer = self.get_object()
#       task_timer.end_time = timezone.now()
#       duration = task_timer.end_time - task_timer.start_time
#       task_timer.total_time = duration
#       task_timer.save()
#       return JsonResponse({'message': 'Successfully stopped task time'}, status=200)
#     else:
#       return JsonResponse({
#         'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
#         'result': 'Not Allowed',
#         'message': 'Must be a POST method',
#       })

#   @csrf_exempt
#   def pause(self, request, pk=None):
#     if request.method == 'POST':
#       task_timer = self.get_object()
#       duration = timezone.now() - task_timer.start_time
#       task_timer.total_time += duration
#       task_timer.save()
#       return JsonResponse({'message': 'Successfully paused task time'}, status=200)
#     else:
#        return JsonResponse({
#         'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
#         'result': 'Not Allowed',
#         'message': 'Must be a POST method',
#       })

#   @csrf_exempt
#   def resume(self, request, pk=None):
#     if request.method == 'POST':
#       task_timer = self.get_object()
#       task_timer.start_time = timezone.now()
#       task_timer.save()
#       return JsonResponse({'message': 'Temps de tâche repris avec succès'}, status=200)
#     else:
#        return JsonResponse({
#         'code': settings.HTTP_CONSTANTS['NOT_ALLOWED'],
#         'result': 'Not Allowed',
#         'message': 'Must be a POST method',
#       })
      