# -*- coding: utf-8 -*-
"""
Django settings for greenwood_history project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os
import sys
import logging
from os.path import join
from pathlib import Path

# import pgconnection
from configurations import Configuration, values
from django_cache_url import BACKENDS

logger = logging.getLogger(__name__)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(join(BASE_DIR, "apps"))
# sys.path.append(join(BASE_DIR, "utils"))

# monkey patch new django redis backend
# monkey patch new django redis backend, can be removed once django_cache_url updates
BACKENDS.update({"django-redis": "django.core.cache.backends.redis.RedisCache"})


class Common(Configuration):
    BASE_DIR = BASE_DIR

    # SECRET CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
    # Note: This key only used for development and testing.
    #       In production, this is changed to a values.SecretValue() setting
    SECRET_KEY = values.SecretValue()
    # END SECRET CONFIGURATION

    # DEBUG
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(False)
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
    TEMPLATE_DEBUG = DEBUG
    # END DEBUG

    ALLOWED_HOSTS = values.ListValue(["*"])
    ROOT_DOMAIN = values.Value()

    # APP CONFIGURATION
    DJANGO_APPS = (
        "pghistory.admin",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.gis",
        # "django.contrib.sites",
    )

    THIRD_PARTY_APPS = (
        "django_extensions",
        "django_filters",
        "rest_framework",
        "rest_framework_gis",
        "pghistory",
        "pgtrigger",
        # "pgconnection",
    )

    LOCAL_APPS = (
        "addresses",
        "buildings",
        "entities",
        "shapes",
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
    # END APP CONFIGURATION

    # MIDDLEWARE CONFIGURATION
    # MIDDLEWARE = values.BackendsValue([
    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]
    # END MIDDLEWARE CONFIGURATION

    # EMAIL CONFIGURATION
    EMAIL_BACKEND = values.Value("django.core.mail.backends.smtp.EmailBackend")
    # END EMAIL CONFIGURATION

    # MANAGER CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
    ADMINS = values.SingleNestedTupleValue()

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
    # MANAGERS = values.SingleNestedTupleValue()
    # END MANAGER CONFIGURATION

    # DATABASE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
    DATABASES = values.DatabaseURLValue("postgres://localhost/greenwood_history")
    # END DATABASE CONFIGURATION

    # CACHING
    CACHES = values.CacheURLValue("locmem://greenwood_history")
    # END CACHING

    # GENERAL CONFIGURATION

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
    TIME_ZONE = "America/Chicago"

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
    LANGUAGE_CODE = "en-us"

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
    SITE_ID = None

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
    USE_I18N = True

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
    USE_L10N = True

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
    USE_TZ = True
    # END GENERAL CONFIGURATION

    # TEMPLATE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
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

    # STATIC FILE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
    STATIC_ROOT = join(os.path.dirname(BASE_DIR), "staticfiles")

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
    STATIC_URL = "/static/"

    # See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
    # STATICFILES_DIRS = (
    #     join(BASE_DIR, "static"),
    # )

    # See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
    # STATICFILES_FINDERS = (
    #     "django.contrib.staticfiles.finders.FileSystemFinder",
    #     "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # )
    # END STATIC FILE CONFIGURATION

    # MEDIA CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
    MEDIA_ROOT = join(BASE_DIR, "media")

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
    MEDIA_URL = "/media/"
    # END MEDIA CONFIGURATION

    # URL Configuration
    ROOT_URLCONF = "greenwood_history.urls"

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
    WSGI_APPLICATION = "greenwood_history.wsgi.application"
    ASGI_APPLICATION = "greenwood_history.asgi.application"
    # End URL Configuration

    # AUTHENTICATION CONFIGURATION
    AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

    # "rest_framework_simplejwt.authentication.JWTAuthentication",
    # Password validation
    # https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

    # END AUTHENTICATION CONFIGURATION

    # LOGGING CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
    # A sample logging configuration. The only tangible logging
    # performed by this configuration is to send an email to
    # the site admins on every HTTP 500 error when DEBUG=False.
    # See http://docs.djangoproject.com/en/dev/topics/logging for
    # more details on how to customize your logging configuration.

    # fmt: off
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": True,
        "filters": {
            "require_debug_false": {
                "()": "django.utils.log.RequireDebugFalse",
            },
            "require_debug_true": {
                "()": "django.utils.log.RequireDebugTrue",
            },
        },
        "formatters": {
            "django.server": {
                "()": "django.utils.log.ServerFormatter",
                "format": "[{server_time}] {message}",
                "style": "{",
            },
            "rich": {
                "datefmt": "[%X]",
                "rich_tracebacks": True
            }
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "filters": ["require_debug_true"],
                "class": "logging.StreamHandler",
            },
            "rich": {
                "class": "rich.logging.RichHandler",
                "filters": ["require_debug_true"],
                "formatter": "rich",
                "level": "DEBUG",
            },
            "django.server": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "django.server",
            },
            "mail_admins": {
                "level": "ERROR",
                "filters": ["require_debug_false"],
                "class": "django.utils.log.AdminEmailHandler"
            }
        },
        "loggers": {
            "": {
                "handlers": ["rich"],
                "level": os.getenv('DJANGO_LOG_LEVEL', 'WARNING'),
            },
        }
    }
    # fmt: on
    # END LOGGING CONFIGURATION

    REST_FRAMEWORK = {
        "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
        "PAGE_SIZE": 10,
        "DEFAULT_FILTER_BACKENDS": [
            "django_filters.rest_framework.DjangoFilterBackend",
            "rest_framework.filters.SearchFilter",
        ],
    }
