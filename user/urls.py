from django.urls import path

from . import views

urlpatterns = [
    path('add', views.register, name='register'),
    path('', views.get_users, name='get_users'),
    path('<int:user_id>', views.get_user, name='get_user'),
    path('login', views.login, name='login'),
    path('delete/<int:user_id>', views.delete_user , name='delete_user')
]
