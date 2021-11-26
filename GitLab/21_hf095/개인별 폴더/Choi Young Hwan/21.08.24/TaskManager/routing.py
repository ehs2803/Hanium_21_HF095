from django.urls import path

from TaskManager import consumers

websocket_urlpatterns = [
    path('ws/test', consumers.ChatConsumer.as_asgi()),
    path('ws/Drowsiness', consumers.ChatConsumer.as_asgi()),
    path('ws/TaskManager', consumers.ChatConsumer.as_asgi()),
    path('ws/Blinking', consumers.ChatConsumer.as_asgi()),
]
