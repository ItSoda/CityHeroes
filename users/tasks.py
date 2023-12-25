import uuid
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from users.models import EmailVerifications, Users


@shared_task
def send_email_verify_task(user_id):
    user = Users.objects.get(id=user_id)
    print("goood")
    expiration = now() + timedelta(hours=24)
    record = EmailVerifications.objects.create(
        code=uuid.uuid4(), user=user, expiration=expiration
    )
    record.send_verification_email()