import uuid
from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from users.models import EmailVerification, User


# По любым вопросам к доке https://docs.djangoproject.com/en/4.2/ref/signals/
@receiver(post_save, sender=User)
def user_post_save(created, **kwargs):
    instance = kwargs["instance"]
    if created:
        user = User.objects.get(id=instance.id)
        expiration = now() + timedelta(hours=24)
        record = EmailVerification.objects.create(
            code=uuid.uuid4(), user=user, expiration=expiration
        )
        record.send_verification_email()