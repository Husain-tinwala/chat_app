import os

from django.core.asgi import get_asgi_application

from django.urls import path

from channels.routing import ProtocolTypeRouter,URLRouter

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator


from app.consumers import OnlineStatusConsumer, PersonalChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app.settings')

application= ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter([
            path('ws/<int:id>/',PersonalChatConsumer.as_asgi()),
            path('ws/online/',OnlineStatusConsumer.as_asgi())
        ]))
        ),
})