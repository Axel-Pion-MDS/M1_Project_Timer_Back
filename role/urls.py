
from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_roles, name='get_roles'),
    path('<int:role_id>', views.get_role, name='get_role'),
    path('add', views.add_role, name='add_role'),
    path('update', views.update_role, name='update_role'),
    path('delete/<int:role_id>', views.delete_role, name='delete_role'),
]
