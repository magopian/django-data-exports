DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'foo',
    },
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.formtools',
    'django.contrib.markup',
    'data_exports',
]

SECRET_KEY = '0'
ROOT_URLCONF = 'data_exports.test_urls'
STATIC_URL = 'foo/'
