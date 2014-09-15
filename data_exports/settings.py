DEBUG = True
TEMPLATE_DEBUG = True
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3',
                         'NAME': 'test.sqlite'}}
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'data_exports',
    'south',
]
SECRET_KEY = "not really secret, is it?"
ROOT_URLCONF = 'data_exports.test_urls'
