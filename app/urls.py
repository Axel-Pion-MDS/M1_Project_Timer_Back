"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include, re_path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('role/', include('role.urls')),
    path('organization/', include('organization.urls')),
    path('user-organization/', include('user_organization.urls')),
    path('team/', include('team.urls')),
    path('project/', include('project.urls')),
    path('task/', include('task.urls')),
    path('user-task/', include('user_task.urls')),
    path('token/', views.send_csrf_token, name="send_csrf_token"),
    path('', include('swagger_ui.urls')),
    path('', lambda request: redirect('api-doc/', permanent=True)),
]
