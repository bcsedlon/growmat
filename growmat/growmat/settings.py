"""
Django settings for growmat project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v@+#1joq*u0)3)njh24sw)5*ddip==@#&6(2g%99d*@as$8@oy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'djangosecure',
	#'dbbackup',
	'w',
#    'mod_wsgi.server',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    #'djangosecure.middleware.SecurityMiddleware',
)

ROOT_URLCONF = 'growmat.urls'

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

WSGI_APPLICATION = 'growmat.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'ramdisk/db.sqlite3'),
		#'NAME': os.path.join('/home/pi/growmat/ramdisk/', 'db.sqlite3'),
	'OPTIONS': {
            'timeout': 30,
        }
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/Prague'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

#STATIC_URL = '/w/static/w/'
STATIC_URL = '/static/'

# sev 
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'ramdisk'),
    os.path.join(BASE_DIR, 'archives'),
    os.path.join(BASE_DIR, 'archives', '0'),
    os.path.join(BASE_DIR, 'archives', '1'),
    os.path.join(BASE_DIR, 'archives', '2'),
    os.path.join(BASE_DIR, 'archives', '3'),
    os.path.join(BASE_DIR, 'archives', '4'),
    os.path.join(BASE_DIR, 'archives', '5'),
    os.path.join(BASE_DIR, 'archives', '6'),
    os.path.join(BASE_DIR, 'archives', '7'),
    os.path.join(BASE_DIR, 'archives', '8'),
    os.path.join(BASE_DIR, 'archives', '9'),
    os.path.join(BASE_DIR, 'archives', '10'),   
    os.path.join(BASE_DIR, 'archives', '11'),   
    os.path.join(BASE_DIR, 'archives', '12'),   
    os.path.join(BASE_DIR, 'archives', '13'),   
    os.path.join(BASE_DIR, 'archives', '14'),   
    os.path.join(BASE_DIR, 'archives', '15'),   
    os.path.join(BASE_DIR, 'archives', '16'),   
    os.path.join(BASE_DIR, 'archives', '17'),   
    os.path.join(BASE_DIR, 'archives', '18'),   
    os.path.join(BASE_DIR, 'archives', '19'),   
]

DBBACKUP_BACKUP_DIRECTORY = '/home/pi/growmat/'
DBBACKUP_FILENAME_TEMPLATE = 'dbbackup'

LOGIN_REDIRECT_URL = '/w/'

#SECURE_SSL_REDIRECT = True
