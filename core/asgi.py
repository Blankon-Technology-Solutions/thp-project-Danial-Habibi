import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import todo.routing  # Import your app's routing configuration

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Define WebSocket URL patterns
websocket_urlpatterns = todo.routing.websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Default HTTP routing
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
