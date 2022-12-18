from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_user_tasks, name='get_user_tasks'),
    path('<int:user_task_id>', views.get_user_task, name='get_user_task'),
    path('users/<int:task_id>', views.get_users_from_task, name='get_users_from_task'),
    path('add', views.add_user_to_task, name='add_user_to_task'),
    path('update', views.update_user_role_from_task, name='update_user_role_from_task'),
    path('delete', views.delete_user_from_task, name='delete_user_from_task'),
]
