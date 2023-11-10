from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import FormAnimal


@receiver(post_save, sender=FormAnimal)
def formanimal_post_save(created, **kwargs):
    instance = kwargs["instance"]
    if created:
        subjects = (
            f"CityHeroes | Успешная заявка на аккаунте {instance.user.email}"
        )
        message = "Поздравляем, вы подали заявку на нашем сайте на получение {instance.animal.name}\n CityHeroes"
        send_mail(
            subject=subjects,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.user.email],
            fail_silently=False,
        )
