from celery import shared_task

from users.models import EmailVerifications, Users

from .models import FormAnimals

@shared_task
def send_form_email(form_id):
    form = FormAnimals.objects.get(id=form_id)
    user = Users.objects.get(id=form.user.id)
    record = EmailVerifications.objects.create(user=user)

    record.send_form_email()


@shared_task
def update_user(form_id):
    form = FormAnimals.objects.get(id=form_id)
    user = Users.objects.get(id=form.user.id)
    
    user.quantity_forms += 1
    user.forms.add(form)
    user.save()
