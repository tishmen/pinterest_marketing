import os

import djcelery

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PHOTO_DIR = os.path.join(BASE_DIR, 'data', 'photo')

ERROR_DIR = os.path.join(BASE_DIR, 'bot', 'error')

SECRET_KEY = '(zj-3#0@5z=_lnm!!%+$u4oqy=msid9*2dy9_un3-uwb^v^766'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'constance',
    'djcelery',
    'import_export',
    'bot',
    'data',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'pinterest_marketing.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

WSGI_APPLICATION = 'pinterest_marketing.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Skopje'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'log'),
        },
    },
    'loggers': {
        'pinterest_marketing': {
            'handlers': ['file'],
            'level': 'DEBUG',
        }
    }
}

CONSTANCE_CONFIG = {
    'MINIMUM_REPIN_COUNT': (1, 'Minimum repin count for pin'),
    'MINIMUM_LIKE_COUNT': (0, 'Minimum like count for pin'),
    'MINIMUM_COMMENT_COUNT': (0, 'Minimum comment count for pin'),
    'MINIMUM_PIN_COUNT': (1, 'Minimum pin count for board'),
    'MINIMUM_BOARD': (1, 'Minimum boards per task run'),
    'MAXIMUM_BOARD': (1, 'Maximum boards per task run'),
    'MINIMUM_LIKE': (1, 'Minimum likes per task run'),
    'MAXIMUM_LIKE': (1, 'Maximum likes per task run'),
    'MINIMUM_COMMENT': (1, 'Minimum comments per task run'),
    'MAXIMUM_COMMENT': (1, 'Maximum comments per task run'),
    'MINIMUM_REPIN': (1, 'Minimum repins per task run'),
    'MAXIMUM_REPIN': (1, 'Maximum repins per task run'),
    'MINIMUM_FOLLOW': (1, 'Minimum follows per task run'),
    'MAXIMUM_FOLLOW': (1, 'Maximum follows per task run'),
    'MINIMUM_UNFOLLOW': (1, 'Minimum unfollows per task run'),
    'MAXIMUM_UNFOLLOW': (1, 'Maximum unfollows per task run'),
    'MINIMUM_SCRAPE': (1, 'Minimum scrapes per task run'),
    'MAXIMUM_SCRAPE': (1, 'Maximum scrapes per task run'),
}

SUIT_CONFIG = {
    'ADMIN_NAME': 'Pinterest Marketing',
}

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_SEND_EVENTS = True
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

djcelery.setup_loader()
