"""
ASGI config for portfolio project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

if os.environ.get('DEBUG') == 'True':
    application = ProtocolTypeRouter({
        'http':
        ASGIStaticFilesHandler(get_asgi_application()),

    })
else:
    application = ProtocolTypeRouter({
        'http':
        get_asgi_application(),
    })
