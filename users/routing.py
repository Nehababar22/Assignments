from django.urls import re_path
from . import consumers

# WebSocket URL patterns for the application
websocket_urlpatterns = [
    re_path(r'ws/chat/single-room/$', consumers.ChatConsumer.as_asgi()),
]