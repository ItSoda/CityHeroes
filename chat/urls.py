from django.urls import path

from . import views

urlpatterns = [
    path("test/", views.test),
    path("", views.chat, name="room"),
    path("room", views.index, name="index"),
]
