"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

from .madval1369_secret import *





# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'harchi'
# مقداری که اینجا بود رو به اون صورت داخل فایل docker-compose.yml می نویسیم و دقت کنم که
# علامت $ هر جا بود باید یه $ دیگه کنارش بنویسیم. چون برای داکر کامپوز اسکیپ کاراکتر هست.

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']#, '.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party apps
    'debug_toolbar',

    # allauth
    'allauth',
    'allauth.account',

    # allauth extra social accounts
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.linkedin_oauth2',

    'rosetta',

    # local apps
    'accounts',
    'confectionery',

]

MIDDLEWARE = [
    # debug toolbar
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # allauth
    "allauth.account.middleware.AccountMiddleware",
]

# allauth مربوط به اضافه کردن شبکه های اجتماعی
# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'APP': {
            'client_id': GITHUB_CLIENT_ID,
            'secret': GITHUB_CLIENT_SECRET,
        },
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
    },
    "openid_connect": {
        "APPS": [
            {
                "provider_id": "linkedin",
                "name": "LinkedIn",
                "client_id": LINKED_IN_CLIENT_ID,
                "secret": LINKED_IN_CLIENT_SECRET,
                "settings": {
                    "server_url": "https://www.linkedin.com/oauth",
                },
            }
        ]
    },
}

# all auth مرتبط با تنظیمات
ACCOUNT_SESSION_REMEMBER = True # تیک ریممبر می رو به صورت پیش فرض فعال میذاره و دیگه به کاربر هم نشون نمیده.
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False # موقع ثبت نام ۲ بار از ما رمز رو میخواد که وارد کنیم. به صورت پیش فرض مقدارش ترو هست. اگه فالسش کنیم یه بار میپرسه
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_ATHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True

AUTH_USER_MODEL = 'accounts.CustomUser'

ROOT_URLCONF = 'config.urls'

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

                # `allauth` needs this from django
                'django.template.context_processors.request',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

# allauth مرتبط با
SITE_ID = 1

########################     EMAIL     ########################
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
# EMAIL_USE_SSL = True
# EMAIL_PORT = 465 # SSL
# However, SSL is an older technology that contains some security flaws.
# Transport Layer Security (TLS) is the upgraded version of SSL that fixes existing SSL vulnerabilities.
# TLS authenticates more efficiently and continues to support encrypted communication channels.
# خلاصه این که اس اس ال یه مشکلاتی داشت و ورژن تی ال اس رو دادن که امن تره
EMAIL_USE_TLS = True
EMAIL_PORT = 587 # TLS
EMAIL_HOST_USER = 'shookooljooni254@gmail.com'
EMAIL_HOST_PASSWORD = 'dhbifelfqtxebxgu'
########################     END EMAIL     ########################

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'confectionery',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': 3306
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
# LANGUAGE_CODE = 'fa'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Tehran'

USE_L10N = True

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
