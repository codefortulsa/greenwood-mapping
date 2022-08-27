# -*- coding: utf-8 -*-
"""
Production Configurations
- Debug mode never on
- Meant to be served from digital ocean
"""
from copy import copy

from configurations import values

from .common import Common


class Prod(Common):

    # DEBUG
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
    # END DEBUG

    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    # when not ssl, redirect to ssl

    @property
    def MIDDLEWARE(self):
        # insert whitenoise after django security middleware
        mw = list(copy(Common.MIDDLEWARE))
        mw.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
        return mw

    # server
    USE_X_FORWARDED_HOST = True

    # whitenoise
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    WHITENOISE_MANIFEST_STRICT = False
    WHITENOISE_USE_FINDERS = True
