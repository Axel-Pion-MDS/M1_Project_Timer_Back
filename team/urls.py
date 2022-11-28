from django.urls import path
from team import views

urlpatterns = [
    path('', views.get_teams, name='get_teams'),
    path('<int:team_id>', views.get_team, name='get_team'),
    # path('add', views.add_role, name='add_role'),
    # path('update', views.update_role, name='update_role'),
    # path('delete/<int:role_id>', views.delete_role, name='delete_role'),
]
