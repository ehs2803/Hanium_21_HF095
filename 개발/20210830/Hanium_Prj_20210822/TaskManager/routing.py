from django.urls import path

from TaskManager import consumers

websocket_urlpatterns = [
    path('ws/test', consumers.ChatConsumer.as_asgi()),
]