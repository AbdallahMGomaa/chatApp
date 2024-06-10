"""
ASGI config for chatApp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
import django
import os

from channels.security.websocket import OriginValidator
from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter


from dotenv import load_dotenv
load_dotenv()
django.setup()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatApp.settings')

from messaging.middleware import JWTAuthMiddleware
from messaging.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": OriginValidator(JWTAuthMiddleware(
            URLRouter(websocket_urlpatterns)
        ),
        ['*']
    )
})
