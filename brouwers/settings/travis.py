try:
    from .secrets import *
except ImportError:
    import sys
    sys.exit('secrets.py settings file not found.')

from base import *


# for ease, override here. No production values are used anyway
SECRET_KEY = '04wb^^4e5%djxrpe4_u6*&ska+s(j1=!k2^frlfux2se#$%mox'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':MEMORY:',
    },
    'mysql': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':MEMORY:',
    },
}

# FIXME: get sessionprofile install working on Travis...

THIRD_PARTY_APPS = (
    'django_extensions',
    'django_nose',
    'south',
    'tastypie',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'albums.middleware.UploadifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'banning.middleware.BanningMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)