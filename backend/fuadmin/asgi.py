"""
ASGI config for fuadmin project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fuadmin.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

http_application = get_asgi_application()


# from fuadmin.routing import websocket_urlpatterns
from django.urls import path
from fuadmin.websocketConfig import MegCenter

websocket_urlpatterns = [
    path('ws/<str:service_uid>/', MegCenter.as_asgi()), #consumers.DvadminWebSocket 是该路由的消费者
]

application = ProtocolTypeRouter({
    "http": http_application,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns # 指明路由规则 service_uid 这个是前端传过来的token，需要解码
        )
    ),
})
