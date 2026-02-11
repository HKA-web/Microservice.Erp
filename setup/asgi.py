import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import setup.routings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
os.environ.setdefault('DJANGO_ALLOW_ASYNC_UNSAFE', 'true')
asgi_application = get_asgi_application()

application = ProtocolTypeRouter({
    'http': asgi_application,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            setup.routings.websocket_urlpatterns()
        )
    ),
})
