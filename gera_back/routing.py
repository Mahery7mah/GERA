from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/notification/(?P<evenement_id>\d+)/$', consumers.NotificationConsumer.as_asgi()),
]