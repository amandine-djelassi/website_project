"""
Django settings for trotteurs project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    """
        Get the nevironment variable or return exception
    """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable.".format(var_name)
        raise ImproperlyConfigured(error_msg)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's7&w3=y!_64^82m^=@ui2cz*zk$unrapm*qyl4vr4nms9p*(p-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True



# configure email
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = get_env_variable('EMAIL_ADRESS')
# EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')
# EMAIL_PORT = 587
# EMAIN_SUBJECT_PREFIX = '[Trotteurs]'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# print in the console instead of send an email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# print in a file
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = 'tmp/email-messages/'

ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window;
REGISTRATION_OPEN = True # If True, users can register
REGISTRATION_AUTO_LOGIN = True # If True, the user will be automatically logged in.
LOGIN_REDIRECT_URL = '/' # The page you want users to arrive at after they successful log in
LOGIN_URL = '/accounts/login/' # The page users are directed to if they are not logged in, and are trying to access pages requiring authentication
INCLUDE_REGISTER_URL = True

AUTH_USER_MODEL = 'trotteurs.User'

ALLOWED_HOSTS = ['5.48.217.250','127.0.0.1','.trotteur.tk', 'localhost']


# Application definition
INSTALLED_APPS = [
    'registration',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
    'gallery.apps.GalleryConfig',
    'trotteurs.apps.TrotteursConfig',
    'ckeditor',
    'ckeditor_uploader',
    'django_countries',
    'gunicorn',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'trotteurs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['./templates',],
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

WSGI_APPLICATION = 'trotteurs.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/1.10/topics/i18n/
LANGUAGE_CODE = 'fr-FR'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static_files")
#STATICFILES_DIRS = (os.path.join(BASE_DIR, "blog/static"), )

AVATAR_SIZE = (100, 100)
DEFAULT_AVATAR_URL = STATIC_URL + 'trotteurs/img/avatar.jpg'
# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# CKeditor jquery
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"