from .settings import *

ALLOWED_HOSTS = ['*']
DEBUG = True
INSTALLED_APPS += ['debug_toolbar']
INTERNAL_IPS = ['127.0.0.1', '172.19.0.1']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
ROOT_URLCONF = 'config.urls_dev'
