from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import FormAnimals
from .tasks import send_form_email, update_user


@receiver(post_save, sender=FormAnimals)
def formanimal_post_save(created, instance, **kwargs):
    if created:
        update_user.delay(instance.id)
        send_form_email.delay(instance.id)
