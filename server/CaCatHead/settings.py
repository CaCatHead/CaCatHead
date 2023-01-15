"""
Django settings for server project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
import sys
from datetime import timedelta
from pathlib import Path

from CaCatHead.config import BASE_DIR, cacathead_config

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jve48vpw^1-z+1lc8#u^f@6gai%r)k-m-47^qw$^@nct1u)*^_'

# SECURITY WARNING: don't run with debug turned on in production!
# Enable DEBUG mode by default
DEBUG = False if os.getenv('DEBUG', 'true').lower() == 'false' else True
# Disable DEBUG_JUDGE by default
DEBUG_JUDGE = True if os.getenv('DEBUG_JUDGE', 'false').lower() == 'true' else False

# Root username and password
CACATHEAD_ROOT_USER = cacathead_config.server.root.username
CACATHEAD_ROOT_PASS = cacathead_config.server.root.password

# Testcase root dir
TESTCASE_ROOT = Path(cacathead_config.testcase.root)

# Config rabbit mq connection
RMQ_HOST = cacathead_config.rabbitmq.host
RMQ_PORT = str(cacathead_config.rabbitmq.port)
RMQ_USER = cacathead_config.rabbitmq.username
RMQ_PASS = cacathead_config.rabbitmq.password

# Trusted origin
ALLOWED_HOSTS = ['127.0.0.1'] + cacathead_config.server.allowed_host
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1'] + cacathead_config.server.trusted_origin

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Django REST framework is a powerful and flexible toolkit for building Web APIs.
    # See: https://www.django-rest-framework.org/
    'rest_framework',
    # Authentication Module for django rest auth
    # See: https://github.com/James1345/django-rest-knox
    'knox',
    # See: https://django-cron.readthedocs.io/en/latest/introduction.html
    'django_cron',
    # Custom apps
    'CaCatHead.user.apps.UserConfig',
    'CaCatHead.permission.apps.PermissionConfig',
    'CaCatHead.problem.apps.ProblemConfig',
    'CaCatHead.post.apps.PostConfig',
    'CaCatHead.submission.apps.SubmissionConfig',
    'CaCatHead.contest.apps.ContestConfig',
    'CaCatHead.judge.apps.JudgeConfig'
]

# Django REST framework config
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'knox.auth.TokenAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '5/second',
        'user': '20/second'
    },
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

# django-rest-knox config
REST_KNOX = {
    'TOKEN_TTL': timedelta(days=30),
    'AUTO_REFRESH': True
}

# django cron tasks
CRON_CLASSES = [
    'CaCatHead.judge.cron.PingJudgeNode'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CaCatHead.urls'

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

WSGI_APPLICATION = 'CaCatHead.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / cacathead_config.database.name,
    }
} if cacathead_config.database.engine == 'sqlite' or 'test' in sys.argv else {
    # 如果是测试环境，直接使用 sqlite 不使用 postgresql 或者 mysql
    'default': {
        'ENGINE': 'django.db.backends.' + cacathead_config.database.engine,  # mysql or postgresql
        'NAME': cacathead_config.database.name,
        'USER': cacathead_config.database.username,
        'PASSWORD': cacathead_config.database.password,
        'HOST': cacathead_config.database.host,
        'PORT': cacathead_config.database.port,
    }
}

# Caches
# https://docs.djangoproject.com/zh-hans/4.1/topics/cache/
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    },
    'redis': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://{cacathead_config.redis.host}:{cacathead_config.redis.port}',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime}  {levelname} {process:d} --- {module} ({thread:d}): {message}',
            'style': '{',
        },
        'request': {
            'format': '[{asctime}] {message}',
            'style': '{'
        },
        'judge': {
            'format': '[{asctime}: {type} #{submission.id}] {message}',
            'style': '{'
        },
        'simple': {
            'format': '[{asctime}: {levelname}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'request': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'request'
        },
        'null': {
            'class': 'logging.NullHandler',
        },
        'judge': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'judge'
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django.request': {
            'handlers': ['request'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['request'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['null'],
        },
        'django.db.backends': {
            'handlers': ['null'],
            'level': 'DEBUG',
        },
        'CaCatHead': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'Judge.service': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'Judge.submission': {
            'handlers': ['judge'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

TEST_RUNNER = 'snapshottest.django.TestRunner'
