from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_projects, name='get_projects'),
    path('<int:project_id>', views.get_project, name='get_project'),
    path('add', views.add_project, name='add_project'),
    path('update', views.update_project, name='update_project'),
    path('delete/<int:project_id>', views.delete_project, name='delete_project'),
]
