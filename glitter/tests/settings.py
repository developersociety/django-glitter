# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.utils.crypto import get_random_string


BASE_DIR = os.path.dirname(__file__)


DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

SITE_ID = 1

STATIC_URL = '/static/'

SECRET_KEY = get_random_string(length=50)

ROOT_URLCONF = 'glitter.tests.urls'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'glitter.pages.middleware.PageFallbackMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'glitter',
    'glitter.assets',
    'glitter.blocks.banner',
    'glitter.blocks.form',
    'glitter.blocks.html',
    'glitter.blocks.image',
    'glitter.blocks.redactor',
    'glitter.blocks.related_pages',
    'glitter.pages',
    'glitter.publisher',
    'glitter.reminders',
    'glitter.tests.sample',
    'glitter.tests.sampleblocks',
    'mptt',
    'sorl.thumbnail',
    'taggit',
)

USE_TZ = True


APPEND_SLASH = True


GLITTER_LOGIN_PERMS = True


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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
            ],
        },
    },
]


# Fastest possible password hasher for test users
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
