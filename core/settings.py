from pathlib import Path
import os
import stripe
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+#fr_3a%umwm14ou4*dr)1r@v(iyt4duh9%+b2f_yftp)zlur*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Add Our Custom User

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'items',
    'rating',
    'non_functional_pages',

    # SOCIAL AUTH
    'django.contrib.sites',  # must
    'allauth',  # must
    'allauth.account',  # must
    'allauth.socialaccount',  # must
    'allauth.socialaccount.providers.google',  # new
]


# Custom User MOdel

AUTH_USER_MODEL = 'accounts.MyUser'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'core.urls'

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

# WSGI_APPLICATION = 'core.wsgi.application'

ASGI_APPLICATION = 'core.asgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)


STATIC_URL = '/static/'


# Default primary key field type


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media Files Root
MEDIA_ROOT = BASE_DIR / 'media'


# Email Setting
# SETTING FOR EMAIL SENDING
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'abubakarjutt6346527@gmail.com'
EMAIL_HOST_PASSWORD = 'apiwqxejvqqbnyrq'


# core/settings.py


# All Auth / Social Auth Setting

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

SITE_ID = 3

ACCOUNT_EMAIL_VERIFICATION = 'none'

SOCIALACCOUNT_LOGIN_ON_GET = True

LOGIN_REDIRECT_URL = '/'


# Channel Layer Setting

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Add this line
]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

 # stripe api
STRIPE_PUBLIC_KEY = "pk_test_51PFwrzP6KHAyJDbS7GWVV8xh2WjQvmOkuZXcxZG4tsGPmru6wGacAdzrSE3X4T3bEzjrl2z3pD6kY8JpDy17I4PW00xPdPn6LV"
STRIPE_SECRET_KEY = "sk_test_51PFwrzP6KHAyJDbSvZxbaoBzrmVDr8kHoEEVfwZs27wVABs9TJFEQirTyotR8WKJ90IZuGTP84IbDXPMHlC0KFAb00R7xcWZKs"

stripe.api_key = "sk_test_51PFwrzP6KHAyJDbSvZxbaoBzrmVDr8kHoEEVfwZs27wVABs9TJFEQirTyotR8WKJ90IZuGTP84IbDXPMHlC0KFAb00R7xcWZKs"