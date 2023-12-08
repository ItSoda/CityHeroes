from django.shortcuts import render


def personal_chat(request, user_pk):
    return render(request, "chat/personal_chat.html", {"user_pk": user_pk})