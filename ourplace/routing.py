
# mysite/routing.py
from django.urls import path
from channels.routing import ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from . import consumers

application = ProtocolTypeRouter({

    # Route websockets
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path(r'ws/chat/(?P<canvas_name>\w+)/$', consumers.CanvasConsumer)
        ])
    ),
})

