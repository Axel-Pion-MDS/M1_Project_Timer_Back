from django.urls import path
from . import views

urlpatterns = [
  path('tasks/', views.TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-list'),
  path('tasks/<int:pk>/', views.TaskViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='task-detail'),
  path('tasks/<int:pk>/start/', views.TaskViewSet.as_view({'post': 'start'}), name='task-start'),
  path('tasks/<int:pk>/stop/', views.TaskViewSet.as_view({'post': 'stop'}), name='task-stop'),
  path('tasks/<int:pk>/pause/', views.TaskViewSet.as_view({'post': 'pause'}), name='task-pause'),
  path('tasks/<int:pk>/resume/', views.TaskViewSet.as_view({'post': 'resume'}), name='task-resume'),
]