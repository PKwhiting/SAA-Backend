import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from simplicarbackend.consumers import BiddingConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simplicarsaa.settings')

# Application for handling HTTP and WebSocket requests
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Your Django application
    "websocket": BiddingConsumer.as_asgi(),  # Your WebSocket consumer
})

