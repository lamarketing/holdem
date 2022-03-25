"""Django 4.0.3."""
import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_KEY')

DEBUG = os.environ.get('DEBUG', 'false').lower() in {'true', 'on', '1'}

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1').split(',')

include(
    'components/apps.py',
    'components/middleware.py',
    'components/db.py',
    'components/templates.py',
    'components/auth.py',
    'components/tz.py',
)

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
