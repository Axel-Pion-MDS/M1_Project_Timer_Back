from django.urls import path
from . import views

urlpatterns = [
  path('taskTimer_list/', views.TaskTimerViewSet.as_view({'get': 'list', 'post': 'create'}), name='taskTimer_list'),
  path('taskTimer_list/<int:pk>/', views.TaskTimerViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='taskTimer_list_detail'),
  path('taskTimer_list/<int:pk>/start/', views.TaskTimerViewSet.as_view({'post': 'start'}), name='taskTimer_list_start'),
  path('taskTimer_list/<int:pk>/stop/', views.TaskTimerViewSet.as_view({'post': 'stop'}), name='taskTimer_list_stop'),
  path('taskTimer_list/<int:pk>/pause/', views.TaskTimerViewSet.as_view({'post': 'pause'}), name='taskTimer_list_pause'),
  path('taskTimer_list/<int:pk>/resume/', views.TaskTimerViewSet.as_view({'post': 'resume'}), name='taskTimer_list_resume'),
]