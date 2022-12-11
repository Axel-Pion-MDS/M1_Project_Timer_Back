from django.urls import path
from team import views

urlpatterns = [
    path('', views.get_teams, name='get_teams'),
    path('<int:team_id>', views.get_team, name='get_team'),
    path('add', views.add_team, name='add_team'),
    path('update', views.update_team, name='update_team'),
    path('delete/<int:team_id>', views.delete_team, name='delete_team'),
    path('users/add', views.add_user_team, name='add_user_team'),
    path('users/update', views.update_user_team, name='update_user_team'),
    path('users/delete/<int:user_team_id>', views.delete_user_team, name='delete_user_team')
]
