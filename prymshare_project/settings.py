# prymshare_project/settings.py

import os
from pathlib import Path
import environ

# Initialize django-environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Read .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Get SECRET_KEY from .env file
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = []

FRONTEND_URL = env('FRONTEND_URL')
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', # Required by django-allauth

    # 3rd Party Apps
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google', # For Google Login
    'dj_rest_auth',
    'dj_rest_auth.registration',

    # Local Apps
    'users',
    'pages',
    'storefront',
]

# Required for django-allauth
SITE_ID = 1

# APPEND_SLASH=False

# Custom User Model
AUTH_USER_MODEL = 'users.CustomUser'

ACCOUNT_ADAPTER = 'users.adapters.CustomAccountAdapter'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # CORS Middleware - should be placed as high as possible
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Add the account middleware from allauth
    'allauth.account.middleware.AccountMiddleware',
]

# CORS Configuration - to allow requests from your React frontend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173", 
    "http://localhost:5174", # Your React frontend development server
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'prymshare_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # --- Update the DIRS list here ---
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Tells Django to look in our new templates folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # --- Add this line to make FRONTEND_URL available in templates ---
                'django.template.context_processors.static',
                'prymshare_project.context_processors.frontend_url_context_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'prymshare_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# Defaulting to SQLite for easy setup. Configure your production DB using .env
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# REST Framework and Authentication Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Simple JWT Configuration
SIMPLE_JWT = {
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# dj-rest-auth & allauth Configuration
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_HTTPONLY': False, # Allow frontend to access the token
    'USER_DETAILS_SERIALIZER': 'users.serializers.UserSerializer',
    'REGISTER_SERIALIZER': 'users.serializers.RegisterSerializer',
    'PASSWORD_RESET_USE_SITES_DOMAIN': True,
    'SESSION_LOGIN': True,
}

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Allauth settings

# OLD_PASSWORD_FIELD_ENABLED = True
# LOGOUT_ON_PASSWORD_CHANGE = False

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory' # or 'mandatory'
# ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'allauth.socialaccount.adapter.DefaultSocialAccountAdapter'

ACCOUNT_CONFIRM_EMAIL_ON_GET = True


# Email confirmation settings

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3


SITE_ID = 1
DOMAIN = 'www.prymshare.com'
SITE_NAME = 'Prymshare'

# Google Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'APP': {
            'client_id': env('GOOGLE_CLIENT_ID'),
            'secret': env('GOOGLE_CLIENT_SECRET'),
            'key': '' # Not needed for OAuth2
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Paystack API Keys - to be stored in .env file
PAYSTACK_SECRET_KEY = env('PAYSTACK_SECRET_KEY')
PAYSTACK_PUBLIC_KEY = env('PAYSTACK_PUBLIC_KEY')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'no-reply@prymshare.com'