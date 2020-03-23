
# mysite/routing.py
from django.urls import re_path
from channels.routing import ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from . import consumers

application = ProtocolTypeRouter({

    # Route websockets
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r'^ws/place/(?P<place_name_slug>.+)/$', consumers.CanvasConsumer),
        ])
    ),
})

