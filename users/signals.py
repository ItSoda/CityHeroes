from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Users
from users.tasks import send_email_verify_task


# По любым вопросам к доке https://docs.djangoproject.com/en/4.2/ref/signals/
@receiver(post_save, sender=Users)
def user_post_save(created, instance, **kwargs):
    if created:
        send_email_verify_task.delay(instance.id)
