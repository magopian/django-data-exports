# -*- coding: utf-8 -*-

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'data_exports',
]
SECRET_KEY = "not really secret, is it?"
ROOT_URLCONF = 'data_exports.test_urls'
