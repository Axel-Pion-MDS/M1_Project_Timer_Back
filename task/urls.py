from django.urls import path

from . import views

urlpatterns = [
    path('<int:project_id>', views.get_tasks, name='get_tasks'),
    path('<int:task_id>', views.get_task, name='get_task'),
    path('add', views.add_task, name='add_task'),
    path('update', views.update_task, name='update_task'),
    path('delete/<int:task_id>', views.delete_task, name='delete_task'),
]