# chat/views.py
from django.shortcuts import render


def index(request):
    return render(request, "chats/index.html")

def room(request, room_name):
    return render(request, "chats/room.html", {"room_name": room_name})