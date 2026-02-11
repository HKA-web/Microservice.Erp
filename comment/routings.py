import logging

from channelsmultiplexer import AsyncJsonWebsocketDemultiplexer
from django.urls import re_path

logger = logging.getLogger(__name__)

websocket_urlpatterns = [
    re_path(r'^ws/comment/$', AsyncJsonWebsocketDemultiplexer.as_asgi()),
]
