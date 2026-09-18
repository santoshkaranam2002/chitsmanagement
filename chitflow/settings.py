"""
Django settings for the chitflow project.

Structure mirrors the reference Estatecraft backend:
  - REST API (Django REST Framework)
  - Swagger / OpenAPI docs (drf-yasg)

Database: MongoDB via Djongo, database name "chitflow" — the same
MongoDB server your other backends (estatecraft/hostelmanagement/
laptoservices/spamanagement) already use (localhost:27017).
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-chitflow-dev-key-change-me-in-production'

DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'chitapp',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Allow the Angular dev server (and anything else) to call the API.
CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'chitflow.urls'

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

WSGI_APPLICATION = 'chitflow.wsgi.application'
ASGI_APPLICATION = 'chitflow.asgi.application'


# ----------------------------------------------------------------------
# Database — MongoDB via Djongo. Requires a running MongoDB server
# (matching your existing setup at mongodb://localhost:27017).
# ----------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'chitflow',
        'CLIENT': {
            'host': os.getenv('MONGO_URI'),
        },
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}
