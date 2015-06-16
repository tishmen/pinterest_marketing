import os

import djcelery

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PHOTO_DIR = os.path.join(BASE_DIR, 'store', 'photo')

SECRET_KEY = '(zj-3#0@5z=_lnm!!%+$u4oqy=msid9*2dy9_un3-uwb^v^766'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
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
    'pinterest',
    'store',
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
        'DIRS': [],
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

WSGI_APPLICATION = 'pinterest_marketing.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pinterest_marketing_database',
        'USER': 'pinterest_marketing_database_user',
        'PASSWORD': 'R)+.,n9_\$u"-f`}',
        'HOST': 'localhost',
        'PORT': '',
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

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_SEND_EVENTS = True
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

djcelery.setup_loader()

CONSTANCE_CONFIG = {
    'MINIMUM_REPIN_COUNT': (1, 'Minimum repin count for pin'),
    'MINIMUM_LIKE_COUNT': (1, 'Minimum like count for pin'),
    'MINIMUM_COMMENT_COUNT': (1, 'Minimum comment count for pin'),
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
}
