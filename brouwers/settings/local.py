"""
This file contains your local settings and should not be in Git.
"""
from os.path import join, normpath, dirname, realpath
import sys

try:
    from .secrets import *
except ImportError:
    sys.exit('secrets.py settings file not found.')


from base import *


DEBUG = True

TEMPLATE_DEBUG = DEBUG


# don't cache templates in development
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


### MIDDLEWARE
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'sessionprofile.middleware.SessionProfileMiddleware',
    'albums.middleware.UploadifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # after auth middleware, checks if user is authenticated
    'banning.middleware.BanningMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)


### INSTALLED APPS
THIRD_PARTY_APPS += (
    'debug_toolbar',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


### EMAILING
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = normpath(join(PROJECT_ROOT, 'mails'))


### TESTING
if 'test' in sys.argv:
    # run tests on in-memory sqlite database
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


# try to override with unversioned file
try:
    from local_overrides import *
except ImportError:
    pass