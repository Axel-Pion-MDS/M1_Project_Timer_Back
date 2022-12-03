from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_user_organizations, name='get_user_organizations'),
    path('<int:user_organization_id>', views.get_user_organization, name='get_user_organization'),
    path('users/<int:organization_id>', views.get_users_from_organization, name='get_users_from_organization'),
    path('add', views.add_user_to_organization, name='add_user_to_organization'),
    path('update', views.update_user_from_organization, name='update_user_from_organization'),
    path('delete', views.delete_user_from_organization, name='delete_user_from_organization'),
]