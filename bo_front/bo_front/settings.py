# Django settings for bo_front project.

import os
here = lambda * x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

PROJECT_ROOT = here("..")
root = lambda * x: os.path.join(os.path.abspath(PROJECT_ROOT), *x)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('kiarash', 'kiarashplusplus@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bo_front',                     
        'USER': 'blockedonline',
        'PASSWORD': '',
        'HOST': 'mysql.csail.mit.edu',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    },
    'main': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bo_main',                     
        'USER': 'blockedonline',
        'PASSWORD': '',
        'HOST': 'blockedonline.cm0kouruoi8e.us-east-1.rds.amazonaws.com',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '5432',                                         # Set to empty string for default.
    }
}

DATABASE_ROUTERS = ['bo_front.routers.FrontRouter']


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        #'TIMEOUT': 60,
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django_seo_js.middleware.HashBangMiddleware',  # If you're using #!
    'django_seo_js.middleware.UserAgentMiddleware',  # If you want to detect by user agent
    'bo_apis.middleware.XsSharing',
    #'bo_apis.middleware.ProfileMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)


ROOT_URLCONF = 'bo_front.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'bo_front.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    root("templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'ping',
    'bo_apis',
    'django_seo_js',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : '{"time": "%(asctime)s", "func name":"%(funcName)s", "line no":"%(lineno)d", "level":"%(levelname)s", "message":"%(message)s"}',
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': "/var/log/django/bo_back.log",
            'maxBytes': 50000,
            'formatter': 'standard',
        },
        'sqllogfile':{
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': "/var/log/django/bo_back_sql.log",
            'maxBytes': 50000,
            'formatter': 'standard',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends':{
            'handlers': ['sqllogfile'],
            'level': 'INFO',    
            'propagate': False,
        },
        '': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
        },
    }


SEO_JS_PRERENDER_TOKEN = "vNyGmd1w7CWYKtwFS16w"

if DEBUG:
    CACHE_MIDDLEWARE_SECONDS = 10
else:
    CACHE_MIDDLEWARE_SECONDS = 86400
#CACHE_MIDDLEWARE_ALIAS = "bo_front"

PING_DEFAULT_RESPONSE = "OK"

PING_CHECKS = (
    'ping.checks.check_database_sessions',
    'ping.checks.check_cache_set',
    'ping.checks.check_cache_get',
)
