from .base import *  # NOQA

DEBUG = False

# ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'typeidea_db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'CONN_MAX_AGE': 5 * 60,
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}

ADMINS = MANAGERS = (
    ('姓名', '<邮件地址>'),
)

EMAIL_HOST = '<邮件smtp服务器地址>'
EMAIL_HOST_USER = '<邮箱登录名>'
EMAIL_HOST_PASSEORD = '<邮箱登录密码>'
EMAIL_SUBJECT_PREFIX = '<邮件标题前缀>'
DEFAULT_FORM_EMAIL = '<邮件展示发件人的地址>'
SERVER_EMAIL = '<邮件服务器>'
STATIC_ROOT = '/home/wbc/django_pro/typeidea-env/static_files/'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s %(asctime)s %(module)s:'
                      '%(funcName)s:%(lineno)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/tmp/logs/typeidea.log',
            'formatter': 'default',
            'maxBytes': 1024 * 1024,    # 1M
            'backupCount': 5,
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True
        },
    }
}
