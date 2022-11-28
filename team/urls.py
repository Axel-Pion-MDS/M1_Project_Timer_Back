from django.urls import path
from team import views

urlpatterns = [
    path('', views.get_teams, name='get_teams'),
    path('<int:team_id>', views.get_team, name='get_team'),
    path('add', views.add_team, name='add_team'),
    path('update', views.update_team, name='update_team'),
    # path('delete/<int:role_id>', views.delete_role, name='delete_role'),
]
