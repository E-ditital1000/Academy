"""
Django settings for SMS project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import posixpath
import environ
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Environment variables
env = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o!ld8nrt4vc*h1zoey*wj48x*q0#ss12h=+zh)kk^6b3aygg=!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['edigitalnetwork.tech','ednetwork.onrender.com', '.now.sh', '127.0.0.1', 'localhost']

# change the default user models to our custom model
AUTH_USER_MODEL = 'accounts.User' 

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'django_cleanup',
    
]

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
STATIC_URL = 'https://res.cloudinary.com/dhauchzdq/'
          
cloudinary.config( 
  cloud_name = "dhauchzdq", 
  api_key = "925253475554343", 
  api_secret = "ZUGD48p7y1_ERNIsK9jIybc2hQg" 
)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dhauchzdq',
    'API_KEY': '925253475554343',
    'API_SECRET': 'ZUGD48p7y1_ERNIsK9jIybc2hQg',
}


# Thired party apps
THIRED_PARTY_APPS = [
    'crispy_forms',
    'rest_framework',
    'channels',
]



# Custom apps
PROJECT_APPS = [
    'app.apps.AppConfig',
    'accounts.apps.AccountsConfig',
    'course.apps.CourseConfig',
    'result.apps.ResultConfig',
    'search.apps.SearchConfig',
    'quiz.apps.QuizConfig',
    'payments.apps.PaymentsConfig',

]

# Combine all apps
INSTALLED_APPS = DJANGO_APPS + THIRED_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SMS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                # 'django.template.context_processors.i18n',
                # 'django.template.context_processors.media',
                # 'django.template.context_processors.static',
                # 'django.template.context_processors.tz',
            ],
        },
    },
]

WSGI_APPLICATION = 'SMS.wsgi.application'

ASGI_APPLICATION = "SMS.asgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# -----------------------------
# NOTE: Some model fields may not work on sqlite db, 
# so consider using postgresql instead
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': ('railway'),
        'USER': ('postgres'),
        'PASSWORD':('G41bCd3E*AFag4c1-*BaCAC*Ba154G2G'),
        'HOST': ('roundhouse.proxy.rlwy.net'),
        'PORT': ('58466'),
    }
}

# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['staticfiles']))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# -----------------------------------
# E-mail configuration

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'joannabedella@gmail.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = 'ncfesqwtekvpeghr'  # Your Gmail password or App Password

# crispy config
CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# DRF setup
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ]
}

# Strip payment config
STRIPE_SECRET_KEY = ('')
STRIPE_PUBLISHABLE_KEY = ('')
