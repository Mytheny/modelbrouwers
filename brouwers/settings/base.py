from os.path import abspath, basename, dirname, join, normpath, realpath
from sys import path

### PATH CONFIGURATION
PROJECT_ROOT = dirname(dirname(dirname(realpath(__file__))))
path.append(PROJECT_ROOT)


### DEBUG CONFIGURATION
DEBUG = False

TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = ('127.0.0.1', '62.45.249.44')


### MANAGERS AND ADMINS
ADMINS = (
    ('BBT', 'admins@modelbrouwers.nl'),
)

MANAGERS = ADMINS


### GENERAL CONFIGURATION
SITE_ID = 1

TIME_ZONE = 'Europe/Amsterdam'

USE_L10N = True

DATE_FORMAT = 'd-m-Y'

USE_I18N = True

gettext_noop = lambda s: s

LANGUAGES = (
    ('en', gettext_noop('English')),
    ('nl', gettext_noop('Dutch')),
)

LOCALE_PATHS = (
    normpath(join(PROJECT_ROOT, 'locale')),
)


### USER UPLOADED MEDIA
MEDIA_ROOT = normpath(join(PROJECT_ROOT, 'media'))

MEDIA_URL = '/media/'


### STATIC CONTENT
STATIC_ROOT = normpath(join(PROJECT_ROOT, 'static'))

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    normpath(join(PROJECT_ROOT, 'brouwers', 'static')),
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'


### CONTEXT PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    'django.contrib.messages.context_processors.messages',

    "albums.context_processors.user_is_album_admin",
    "general.context_processors.connection",
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

TEMPLATE_DIRS = (
    join(PROJECT_ROOT, 'templates'),
    join(PROJECT_ROOT, 'brouwers', 'templates'),
)


### MIDDLEWARE CONFIGURATION
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
)


### URLS
ROOT_URLCONF = 'brouwers.urls'


### ALL INSTALLED APPS
DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
    'django_extensions',
    'django_nose',
    'sessionprofile',
    'south',
    'tastypie',
)

LOCAL_APPS = (
    'albums',
    'awards',
    'banning',
    'builds',
    'forum_tools',
    'general',
#    'groepsbouwkalender',
    'kitreviews',
    'migration',
    'online_users',
    'secret_santa',
    'shirts',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


### LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


### AUTHENTICATION & SESSIONS
SESSION_COOKIE_AGE = 6048000 # 10 weeks

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_PROFILE_MODULE = 'general.UserProfile'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'


### MISC

# MIBBIT CHAT
MIBBIT_SETTINGS = '61b92aae9db826980bf63939f88326f9'
IRC_SERVER = 'irc.slacknet.org'
IRC_CHANNEL = '#modelbrouwers.nl'
IRC_DEFAULT_NICK = 'brouwer%3F%3F'

# REGISTRATION ATTEMPT LOGGING AND COUPLING WITH BANS
LOG_REGISTRATION_ATTEMPS = True


### DATABASE ROUTING
DATABASE_ROUTERS = [
    'forum_tools.db_router.ForumToolsRouter',
    # 'general.db_router.SouthRouter',
]


### CACHES
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    # 'memcached': {
    #     'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    #     'LOCATION': '127.0.0.1:11211',
    # },
    # 'database': {
    #     'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
    #     'LOCATION': 'django_cache',
    # },
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    #     'LOCATION': 'unique-snowflake'
    # }
}


### AWARDS
VOTE_END_MONTH = 1
VOTE_END_DAY = 15


### ALBUMS
VALID_IMG_EXTENSIONS = ['.jpg', '.jpeg', '.png']
THUMB_DIMENSIONS = (200, 150, 'thumb_')


### FORUMTOOLS
PHPBB_TABLE_PREFIX = 'phpbb3_'
PHPBB_URL = '/phpBB3'
PHPBB_UID_COOKIE = 'phpbb3_n95r4_u'


### PROJECT HONEYPOT
HONEYPOT_URL = '/scratchy.php'
# Value between 0 and 255, with 0 meaning no threat.
HTTPBL_MIN_THREAT_LEVEL = 10


### WSGI
#WSGI_APPLICATION = 'wsgi.application'


### TESTING
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--detailed-errors',
    '--nologcapture',
]

SOUTH_TESTS_MIGRATE = False  # Make south shut up during tests

# Functional testing
# Selenium and Splinter settings
# SELENIUM_TESTS = True
# SELENIUM_WEBDRIVER = 'phantomjs'  # Can be any of chrome, firefox, phantomjs