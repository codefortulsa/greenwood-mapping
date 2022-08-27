"""
WSGI config for greenwood_history project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from configurations import importer
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenwood_history.config")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenwood_history.settings")

importer.install()

application = get_wsgi_application()
