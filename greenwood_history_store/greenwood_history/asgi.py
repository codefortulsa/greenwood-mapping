"""
ASGI config for greenwood_history project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from configurations import importer
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenwood_history.config")
os.environ.setdefault("DJANGO_CONFIGURATION", "Prod")

importer.install()
# Get asgi application must come before further imports to prevent django model ready errors.
application = get_asgi_application()
