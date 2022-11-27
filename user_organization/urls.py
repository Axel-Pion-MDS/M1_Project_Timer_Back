from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_user_organizations, name='get_user_organizations'),
    path('<int:user_organization_id>', views.get_user_organization, name='get_user_organization'),
    path('add', views.add_user_organization, name='add_user_organization'),
    path('update', views.update_user_organization, name='update_user_organization'),
    path('delete/<int:user_organizationx_id>', views.delete_user_organization, name='delete_user_organization'),
]