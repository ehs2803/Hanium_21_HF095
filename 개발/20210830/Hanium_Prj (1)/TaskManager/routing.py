from django.urls import path

from TaskManager import consumers

websocket_urlpatterns = [
    path('ws/test', consumers.Consumer.as_asgi()),
    path('ws/Drowsiness', consumers.Consumer.as_asgi()),
    path('ws/TaskManager', consumers.Consumer.as_asgi()),
    path('ws/Blinking', consumers.Consumer.as_asgi()),
]
