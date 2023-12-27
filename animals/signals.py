from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import FormAnimals
from .tasks import send_form_email


@receiver(post_save, sender=FormAnimals)
def formanimal_post_save(created, **kwargs):
    instance = kwargs["instance"]
    if created:
        send_form_email.delay(instance.user.id)
