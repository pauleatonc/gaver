from .base import *
from dotenv import load_dotenv
import os

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME_DEV"),
        'USER': os.getenv("DB_USER_DEV"),
        'PASSWORD': os.getenv("DB_PASSWORD_DEV"),
        'HOST': os.getenv("DB_HOST_DEV"),
        'PORT': os.getenv("DB_PORT_DEV"),
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/app/staticfiles/'


# Media files
# Defines the base URL and directory to serve user uploaded files during development
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'