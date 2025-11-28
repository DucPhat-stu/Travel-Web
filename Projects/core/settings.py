from pathlib import Path
import os
from dotenv import load_dotenv

# load .env trước khi đọc biến môi trường
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-change-this')
DEBUG = os.getenv('DEBUG', 'True') == 'True'

if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# ======================
# DATABASE
# ======================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.{}'.format(
            os.getenv('DATABASE_ENGINE', 'sqlite3')
        ),
        'NAME': os.getenv('DATABASE_NAME', 'polls'),
        'USER': os.getenv('DATABASE_USERNAME', 'myprojectuser'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'password'),
        'HOST': os.getenv('DATABASE_HOST', '127.0.0.1'),
        'PORT': os.getenv('DATABASE_PORT', 5432),
    }
}
# ======================
# INSTALLED APPS
# ======================
INSTALLED_APPS = [
    # Django contrib apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project apps
    'core.apps.CoreConfig',
    'users',
    'tours',
    'hotels',
    'flight',
    'bookings',
    'chatbot',
]

# ======================
# MIDDLEWARE
# ======================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ======================
# TEMPLATES
# ======================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# ======================
# STATIC
# ======================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# ======================
# EMAIL, SESSION
# ======================
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

ROOT_URLCONF = 'travel_tourism.urls'
WSGI_APPLICATION = 'core.wsgi.application'
