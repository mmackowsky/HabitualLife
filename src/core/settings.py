import os
from pathlib import Path

import environ
import sentry_sdk
from django.contrib.messages import constants as messages

from .env import env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR.parent, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["*"]

# Poniższe ustawienia mogą być również potrzebne, aby Django generował poprawne linki
# w zależności od tego, jak masz ustawioną konfigurację serwera i proxy.
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_results",
    "django_extensions",
    "colorfield",
]

INSTALLED_EXTENSIONS = [
    "start",
    "users",
    "habits",
    "stats",
    "achievements",
    "notifications",
]

INSTALLED_APPS += INSTALLED_EXTENSIONS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if env("ENVIRONMENT") == "ci":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "ci_db",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": env("DB_HOST"),
            "PORT": env("DB_PORT"),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Media settings
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "media/"

DEFAULT_PROFILE_IMAGE = "user_profile/default.jpg"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = "static/"
STATIC_ROOT = "/var/app/current/src/staticfiles/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    "var/app/current/src/staticfiles/",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MESSAGE_TAGS = {
    messages.DEBUG: "alert-secondary",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

LOGGING_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)

LOGGING_LEVEL = "DEBUG"
LOG_FILE = os.path.join(LOGGING_DIR, "django.log")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": LOGGING_LEVEL,
            "class": "logging.FileHandler",
            "filename": LOG_FILE,
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["file"],
        "level": LOGGING_LEVEL,
    },
}

# Celery
if env("USE_CELERY"):
    CELERY_BROKER_TRANSPORT_URL = env("CELERY_BROKER_TRANSPORT_URL")
    CELERY_TIMEZONE = env("CELERY_TIMEZONE")
    CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")

# Email settings
if env("USE_EMAIL"):
    EMAIL_USE_TLS = True
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_HOST_USER = env("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
    EMAIL_PORT = env("EMAIL_PORT")
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# AWS settings
# if env("USE_AWS"):
#     AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
#     AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
#     AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
#     AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")

# SENTRY
sentry_sdk.init(
    dsn="https://e26d05b7b1788333665e178e301529ae@o4505985866792960.ingest.sentry.io/4506473310322688",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

FIXTURE_DIRS = "fixtures/"
