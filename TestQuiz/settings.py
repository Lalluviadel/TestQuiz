"""
Django settings for TestQuiz project.
"""
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = str(os.getenv('SECRET_KEY'))

DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(' ')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'quizapp',
    'users',
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

ROOT_URLCONF = 'TestQuiz.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'TestQuiz.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'users.QuizUser'
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

STATIC_URL = '/static/'
STATICFILES_DIRS = (BASE_DIR / 'static',)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DOMAIN_NAME = 'http://127.0.0.1:8000'

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = f'{BASE_DIR}/emails'

LEVEL = 'DEBUG'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
    },
    'formatters': {
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s[%(levelname)s] %(asctime)s :: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': LEVEL,
            'class': 'colorlog.StreamHandler',
            'formatter': 'colored',
        },
        'file': {
            'level': LEVEL,
            'class': 'logging.FileHandler',
            'filename': f'{BASE_DIR}/TestQuiz/logging/{LEVEL}_{datetime.today().date()}.log',
            'formatter': 'colored',
        },
    },
    'loggers': {
        '': {
            'level': LEVEL,
            'handlers': ['console', 'file'],
            'propagate': False,
        },
        'django.request': {
            'level': 'WARNING',
            'handlers': ['console', 'file']
        },
        'django.security.*': {
            'level': 'WARNING',
            'handlers': ['console', 'file']
        },
        'django.security.csrf': {
            'level': 'WARNING',
            'handlers': ['console', 'file']
        },
        'loggers.authnapp': {
            'level': 'ERROR',
            'handlers': ['file'],
            'propagate': True
        },
    }
}
