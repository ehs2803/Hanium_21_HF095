"""
ASGI config for Hanium_Prj project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack #추가
from channels.routing import ProtocolTypeRouter, URLRouter #URLRouter 추가
from django.core.asgi import get_asgi_application
import TaskManager.routing # chat import

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Hanium_Prj.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack( # 추가
        URLRouter(
            TaskManager.routing.websocket_urlpatterns,
        )
    ),
})