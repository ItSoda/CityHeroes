from asgiref.sync import sync_to_async
from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from .models import Users, Room, Message


def index(request):
    return render(request, "chat/index.html")


def chat(request):
    return render(request, "chat/room.html",)


def test(request):
    return render(request, "chat/test.html")
