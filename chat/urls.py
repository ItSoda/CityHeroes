from django.urls import path

from . import views

app_name = "chat"


urlpatterns = [
    path("create-room/<str:uuid>/", views.CreateRoom.as_view(), name="create-room"),
    path("chat-admin/", views.ChatAdmin.as_view(), name="chat-admin"),
    path("chat-admin/<str:uuid>/", views.Room.as_view(), name="room"),
]
