
# mysite/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

from . import consumers

application = ProtocolTypeRouter({

    # Route websockets
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r'^ws/place/(?P<place_name_slug>.+)/$', consumers.CanvasConsumer),
        ])
    ),
})

