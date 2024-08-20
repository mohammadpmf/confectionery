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
SECRET_KEY = DJANGO_SECRET_KEY
# مقداری که اینجا بود رو به اون صورت داخل فایل docker-compose.yml می نویسیم و دقت کنم که
# علامت $ هر جا بود باید یه $ دیگه کنارش بنویسیم. چون برای داکر کامپوز اسکیپ کاراکتر هست.

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DJANGO_DEBUG

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']#, '.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # third party apps
    'debug_toolbar',
    'crispy_forms',
    'crispy_bootstrap5',

    # allauth
    'allauth',
    'allauth.account',
    # allauth extra social accounts
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.linkedin_oauth2',
    'allauth.socialaccount.providers.openid_connect', # برای اکانت هایی مثل لینکد این، که از این سرویس استفاده میکنن باید خود اپین آی دی رو هم اضافه کرد.

    'rosetta',
    'jalali_date',
    # "azbankgateways", نصبش کردم. اما درست کار نمیکرد کامنت کردم. کدهاش رو حذف نکردم.

    # local apps
    'accounts',
    'confectionery',
    'cart',
    'django_madval',
    'orders',
    'payment',
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

INTERNAL_IPS = [
    "127.0.0.1",
]

# allauth مربوط به اضافه کردن شبکه های اجتماعی
# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': GOOGLE_CLIENT_ID,
            'secret': GOOGLE_CLIENT_SECRET,
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    },
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
        "OAUTH_PKCE_ENABLED": True,
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
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = True

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

                # Custom Context Processors
                'cart.context_processors.cart',
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
EMAIL_HOST_USER = DJANGO_EMAIL_ADDRESS
EMAIL_HOST_PASSWORD = DJANGO_EMAIL_APP_PASSWORD
########################     END EMAIL     ########################

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DJANGO_DATABASE_NAME,
        'USER': DJANGO_DATABASE_USERNAME,
        'PASSWORD': DJANGO_DATABASE_PASSWORD,
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
LANGUAGE_CODE = 'fa'

# وقتی رزتا رو میذاریم همه زبان ها رو میاره. در حالی که ما افغانستانی و عربی و غیره رو نمیخوایم.
# میتونیم این طوری فقط چیزایی که میخوایم رو بهش بگیم. با این متغیر
LANGUAGES = (
    ('en', 'English'),
    ('fa', 'Persian'),
)

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Tehran'

USE_L10N = True

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# crispy form config
CRISPY_TEMPLATE_PACK = 'bootstrap5'
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'

LOGIN_REDIRECT_URL = 'homepage'
LOGOUT_REDIRECT_URL = 'homepage'

# برای تغییر دادن اسم خطا از ارور به دنجر که با رنگ بوت استرپ در بیاد و کد کمتری
# بنویسیم تو اچ تی ام ال و ویومون این کدها رو اضافه کردم
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

ZARINPAL_MERCHANT_ID = ZARINPAL_MERCHANT_ID_FAKE

########################### az_iranian_bank_gateways ###########################
# AZ_IRANIAN_BANK_GATEWAYS = {
#     "GATEWAYS": {
#         "ZARINPAL": {
#             "MERCHANT_CODE": ZARINPAL_MERCHANT_ID_FAKE,
#             "SANDBOX": 1,  # 0 disable, 1 active
#         },
#         "IDPAY": {
#             "MERCHANT_CODE": "<YOUR MERCHANT CODE>",
#             "METHOD": "POST",  # GET or POST
#             "X_SANDBOX": 1,  # 0 disable, 1 active
#         },
#         "PAYV1": {
#             "MERCHANT_CODE": "<YOUR MERCHANT CODE>",
#             "X_SANDBOX": 1,  # 0 disable, 1 active
#         },
#     },
#     "IS_SAMPLE_FORM_ENABLE": True,  # اختیاری و پیش فرض غیر فعال است
#     "DEFAULT": "ZARINPAL",
#     "CURRENCY": "IRR",  # اختیاری
#     "TRACKING_CODE_QUERY_PARAM": "tc",  # اختیاری
#     "TRACKING_CODE_LENGTH": 16,  # اختیاری
#     "SETTING_VALUE_READER_CLASS": "azbankgateways.readers.DefaultReader",  # اختیاری
#     "BANK_PRIORITIES": [
#         "ZARINPAL",
#         "IDPAY",
#         "PAYV1",
#     ],  # اختیاری
#     "IS_SAFE_GET_GATEWAY_PAYMENT": False,  # اختیاری، بهتر است True بزارید.
#     "CUSTOM_APP": None,  # اختیاری
# }
# USE_X_FORWARDED_HOST = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
########################### End az_iranian_bank_gateways ###########################
