from .base import *  # NOQA

DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'typeidea_db',
#         'USER': 'root',
#         'PASSWORD': 'woaini',
#         'HOST': '127.0.0.1',
#         'PORT': 3306,
#         'CONN_MAX_AGE': 5 * 60,
#         'OPTIONS': {'charset': 'utf8mb4'}
#     }
# }


# INSTALLED_APPS.extend(['xadmin', 'crispy_forms'])

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']
