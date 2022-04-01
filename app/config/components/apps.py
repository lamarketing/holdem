INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'corsheaders',
    'channels',
    'django_celery_beat',

    'abstractuser',

    'cards.apps.CardsConfig',
    'tournaments.apps.TournamentsConfig',
    'tables.apps.TablesConfig',
]
