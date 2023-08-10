import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import bus.game.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bus.config.production")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            bus.game.routing.websocket_urlpatterns
        )
    ),
})
