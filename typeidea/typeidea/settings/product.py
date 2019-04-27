from .base import *   # NOQA

DEBUG = False

ALLOWED_HOSTS = ['*']

# INSTALLED_APPS += [
#
#     'silk',
#
# ]
#
# MIDDLEWARE += [
#
#     'silk.middleware.SilkyMiddleware',
# ]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'typeidea_db',
        'USER': 'root',
        'PASSWORD': '',
        'PORT': 3306,
        'HOST': '127.0.0.1',
        'CONN_MAN_AGE': 5*60,
        'OPTIONS': {'charset': 'utf8mb4'}
    },
}

REDIS_URL = 'redis://127.0.0.1:6379'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'TIMEOUT': 300,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER': 'redis.connection.HiredisParser',
        },
        'CONNECTION_POOL_CLASS': 'redis.connection.BlockingConnectionPool',
    }
}