from django.urls import path

from . import consumers


websocket_urlpatterns = [
    path("ws/", consumers.UserConsumer.as_asgi()),
    path("ws/chat/", consumers.RoomConsumer.as_asgi()),
    path("ws/chat/<int:user_pk>/", consumers.UserChatConsumer.as_asgi())
]
