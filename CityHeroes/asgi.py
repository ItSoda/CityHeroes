"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.conf import settings
from django.core.asgi import get_asgi_application
from django.urls import re_path
from django.views.static import serve

from chat.middleware import JwtAuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CityHeroes.settings")
django.setup()

from chat import routing


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            JwtAuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
        ),
    }
)