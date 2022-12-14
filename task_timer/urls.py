from django.urls import path
from . import views

urlpatterns = [
  path('<int:task_id>/', views.get_task_timers, name='taskTimer_list'),
  path('<int:task_id>/start/', views.start_task_timer, name='start_task_timer'),
  path('<int:task_timer_id>/stop/', views.stop_task_timer, name='stop_task_timer'),
  path('<int:task_timer_id>/delete/', views.delete_task_timer, name='delete_task_timer'),
]