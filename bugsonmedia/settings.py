
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-i4ag0sr=@xb_ut$3=5mu#(m^ea0grs+6m9$$0l)y3gb!-uf0z*'

DEBUG = True

ALLOWED_HOSTS = []



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'quiz',
    'social_django',
]
###########################
# Add these at the bottom of settings.py
AUTHENTICATION_BACKENDS = (
    'social_core.backends.instagram.InstagramOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/home/' 

# Instagram OAuth settings
SOCIAL_AUTH_INSTAGRAM_KEY = 'your-instagram-client-id'
SOCIAL_AUTH_INSTAGRAM_SECRET = 'your-instagram-client-secret'
SOCIAL_AUTH_INSTAGRAM_EXTRA_DATA = ['user_profile']

SOCIAL_AUTH_INSTAGRAM_AUTH_EXTRA_ARGUMENTS = {
    'scope': 'user_profile',
    'auth_type': 'rerequest'  # THIS IS CRUCIAL
}


SOCIAL_AUTH_SANITIZE_REDIRECTS = True
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

#######3#



TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bugsonmedia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['TEMPLATE_DIR'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'bugsonmedia.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres.ettjpvzvcfprwunkfrza',
        'PASSWORD': 'PT3FV5v1rfeBv4ll',
        'HOST': 'aws-0-ap-south-1.pooler.supabase.com',
        'PORT': '6543',
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




LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'quiz/static'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
