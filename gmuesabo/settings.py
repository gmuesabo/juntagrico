"""
Django settings for gmuesabo project.
"""

import os
from pathlib import Path

from juntagrico import defaults

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('JUNTAGRICO_SECRET_KEY')

DEBUG = os.environ.get("JUNTAGRICO_DEBUG", 'False')=='True'

if not DEBUG:
    ALLOWED_HOSTS = ['gmuesabo.juntagrico.science']

ADMINS = (
    ('Admin', os.environ.get('JUNTAGRICO_ADMIN_EMAIL')),
)
MANAGERS = ADMINS

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {'format': '[%(asctime)s] %(levelname)s %(message)s'}
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
    },
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'juntagrico.apps.JuntagricoAdminConfig',
    'gmuesabo',
    'juntagrico_billing',
    'juntagrico',
    'import_export',
    'impersonate',
    'crispy_forms',
    'crispy_bootstrap4',
    'adminsortable2',
    'polymorphic',
    'django_select2',
    'djrichtextfield',
]

ROOT_URLCONF = 'gmuesabo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'juntagrico.context_processors.vocabulary',
            ],
            'debug' : DEBUG,
        },
    },
]

WSGI_APPLICATION = 'gmuesabo.wsgi.application'

# HTTP

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'impersonate.middleware.ImpersonateMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware'
]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('JUNTAGRICO_DATABASE_ENGINE','django.db.backends.sqlite3'), 
        'NAME': os.environ.get('JUNTAGRICO_DATABASE_NAME','gmuesabo.db'), 
        'USER': os.environ.get('JUNTAGRICO_DATABASE_USER'),
        'PASSWORD': os.environ.get('JUNTAGRICO_DATABASE_PASSWORD'),
        'HOST': os.environ.get('JUNTAGRICO_DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('JUNTAGRICO_DATABASE_PORT', False),
    }
}

# Email

# disable emails for now
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = os.environ.get('JUNTAGRICO_EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('JUNTAGRICO_EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('JUNTAGRICO_EMAIL_PASSWORD')
EMAIL_PORT = int(os.environ.get('JUNTAGRICO_EMAIL_PORT', '25'))
EMAIL_USE_TLS = os.environ.get('JUNTAGRICO_EMAIL_TLS', 'False')=='True'
EMAIL_USE_SSL = os.environ.get('JUNTAGRICO_EMAIL_SSL', 'False')=='True'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'de'
DATE_INPUT_FORMATS =['%d.%m.%Y']

TIME_ZONE = 'Europe/Zurich'
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# django.contrib.staticfiles
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

# django.contrib.sites Settings

SITE_ID = 1


# django.contrib.auth Settings

AUTHENTICATION_BACKENDS = (
    'juntagrico.util.auth.AuthenticateWithEmail',
    'django.contrib.auth.backends.ModelBackend'
)

LOGIN_REDIRECT_URL = "/"


# impersonate Settings

IMPERSONATE = {
    'REDIRECT_URL': '/my/profile',
}


# crispy_form Settings

CRISPY_TEMPLATE_PACK = 'bootstrap4'


# import_export Settings

IMPORT_EXPORT_EXPORT_PERMISSION_CODE = 'view'


# Rich text editor settings

DJRICHTEXTFIELD_CONFIG = defaults.richtextfield_config(LANGUAGE_CODE)


# juntagrico Settings

ORGANISATION_NAME = "gmüesabo"
ORGANISATION_LONG_NAME = "gmüesabo"
ORGANISATION_NAME_CONFIG = {"type": "Genossenschaft", "gender": "f"}
ORGANISATION_ADDRESS = {
    "name":"Genossenschaft gmüesabo",
    "street" : "Lagerplatz",
    "number" : "13",
    "zip" : "8400",
    "city" : "Winterthur",
    "extra" : "c/o machwerk"
}
ORGANISATION_BANK_CONNECTION = {
    "PC" : "46-110-7",
    "IBAN" : "CH78 0839 0033 6959 1000 0",
    "BIC" : "ABSOCH22",
    "NAME" : "Alternative Bank Schweiz AG"
}
ORGANISATION_WEBSITE = {
    'name': "gmuesabo.ch",
    'url': "https://gmuesabo.ch"
}

CONTACTS = {
    "general": "info@gmuesabo.ch"
}

BUSINESS_REGULATIONS = 'https://gmuesabo.ch/site/files/Betriebsreglement_gmuesabo_19052019.pdf'
BYLAWS = 'https://gmuesabo.ch/site/files/Statuten_gmuesabo_26.5.2018.pdf'
FAQ_DOC = 'https://gmuesabo.ch/site/index.php/faq'
ACTIVITY_AREA_INFO = 'https://gmuesabo.ch/site/files/gmuesabo_mitarbeitsmoeglichkeiten.pdf'

BUSINESS_YEAR_CANCELATION_MONTH = 10
MEMBERSHIP_END_MONTH = 12
MEMBERSHIP_END_NOTICE_PERIOD = 6

ENABLE_SHARES = True
SHARE_PRICE = "100"

ASSIGNMENT_UNIT = 'HOURS'

FIRST_JOB_INFO = []

VOCABULARY = {
    'package': 'Korb',
    'from': '{} vom {}'
}

STYLES = {'static': ['gmuesabo/css/customize.css']}

FROM_FILTER = {
    'filter_expression': r'.*@gmuesabo\.ch',
    'replacement_from': 'system@gmuesabo.ch'
}

# Juntagrico billing

BILLS_USERMENU = True
