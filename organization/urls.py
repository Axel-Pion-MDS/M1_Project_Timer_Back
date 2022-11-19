from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_organizations, name='get_organizations'),
    path('/<int:organization_id>', views.get_organization, name='get_organization'),
    path('/add', views.add_organization, name='add_organization'),
    path('/update', views.update_organization, name='update_organization'),
    path('/delete/<int:organizationx_id>', views.delete_organization, name='delete_organization'),
]
