"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from environs import Env
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2z3)o%t-v_aa*kt5t*it&*a53hu454$ceb*jm#b!ikw-pqzm$)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '0.0.0.0',
    '*',
]

# Application definition

INSTALLED_APPS = [
    "corsheaders",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user.apps.UserConfig',
    'role.apps.RoleConfig',
    'organization.apps.OrganizationConfig',
    'user_organization.apps.UserOrganizationConfig',
    'project.apps.ProjectConfig',
    'team.apps.TeamConfig',
    'task.apps.TaskConfig',
    'task_timer.apps.TaskTimerConfig',
    'user_task.apps.UserTaskConfig',

]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://127.31.0.1:3000",
    "http://172.31.0.1:3000",
    "http://localhost:3000"
]

CORS_ORIGIN_WHITELIST = [
    "http://127.0.0.1:3000",
    "http://172.31.0.1:3000",
    "http://localhost:3000"
]

CORS_ALLOW_HEADERS = [    'Authorization',    'Content-Type',"*"]
CORS_ALLOW_METHODS = [    'GET',    'POST',    'PUT', 'PATCH' ,  'DELETE',    'OPTIONS',]   
ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'postgres-db',
        'PORT': 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Constants
HTTP_CONSTANTS = {
    'SUCCESS': 200,
    'CREATED': 201,
    'BAD_REQUEST': 400,
    'UNAUTHENTICATED': 401,
    'FORBIDDEN': 403,
    'NOT_FOUND': 404,
    'NOT_ALLOWED': 405,
    'INTERNAL_SERVER_ERROR': 500,
}

ROLES = {
    'ROLE_USER': 1,
    'ROLE_ADMIN': 2,
    'ROLE_SUPER_ADMIN': 3,
    'ROLE_ORGANIZATION_OWNER': 4,
    'ROLE_ORGANIZATION_CO_OWNER': 5,
    'ROLE_ORGANIZATION_MEMBER': 6,
    'ROLE_TEAM_LEADER': 7,
    'ROLE_TEAM_MEMBER': 8,
}

env = Env()
env.read_env()
TOKEN_KEY = env("JWT_TOKEN_KEY")

