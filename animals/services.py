from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.timezone import now


def animal_search(query):
    from animals.models import Animals

    animals = Animals.objects.filter(name__icontains=query)
    return animals


# EMAIL
def send_form_email(user_email):
    subjects = f"Анкета создана, {user_email}! Скоро вам позвонит специалист "
    message = f"Поздравляем вас!"
    send_mail(
        subject=subjects,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
    )
