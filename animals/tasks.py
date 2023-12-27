from celery import shared_task

from users.models import EmailVerifications, Users


@shared_task
def send_form_email(user_id):
    user = Users.objects.get(id=user_id)
    print("doo")
    record = EmailVerifications.objects.create(user=user)

    record.send_form_email()
