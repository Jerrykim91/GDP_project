"""
Django settings for GDP_project project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=+uhi8o%nf-9w+v4=m-h7yfclxk)%73hpb&6a6gymd(mmoep9i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [

    'member',
    # test
    'service',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

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

ROOT_URLCONF = 'GDP_project.urls'

# 템플릿 경로 추가 
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR), 'templates'], 
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

WSGI_APPLICATION = 'GDP_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        # sqlite DB사용시
            #'ENGINE': 'django.db.backends.sqlite3',
            #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

            #  mysql
            # 'ENGINE': 'django.db.backends.mysql',
            # 'NAME': 'DB명',
            # 'USER': '아이디명',
            # 'PASSWORD' : '암호',
            # 'HOST' : '127.0.0.1',
            # 'PORT' : '포토번호'

            # oracle
            # 'ENGINE': 'django.db.backends.oracle',
            # 'NAME': 'xe', #SID
            # 'USER': 'admin',
            # 'PASSWORD' : '1234',
            # 'HOST' : '192.168.99.100',
            # 'PORT' : '32764'

            # GDP_PROJECT
            'ENGINE': 'django.db.backends.oracle',
            'NAME': 'xe',
            'USER' : 'GDP_PROJECT',
            'PASSWORD' : '1234',
            'HOST' : '192.168.99.100',
            'PORT' : '32764'


            # 'ENGINE': 'django.db.backends.sqlite3',
            # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
# 옵션 추가 
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTION': {'user_attributes': ('username', 'name')},
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
# https://docs.djangoproject.com/en/2.2/howto/static-files/ㄴ

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# 만든 모델을 명시
AUTH_USER_MODEL="member.LIST"
# 인증 확인 실패시 리다이렉트할 경로
LOGIN_URL = '/sign_in/'
# 브라우저를 종료하면 세션이 종료
SESSION_EXPIRE_AT_BROWSER_CLOSE = True