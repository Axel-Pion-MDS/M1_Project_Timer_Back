from django.urls import path

from . import views

urlpatterns = [
    path('add', views.add_user, name='add_user'),
]
