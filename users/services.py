from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.timezone import now


# MODELS METHODS
# EMAIL VERIFICATION
def send_verification_email(user_email, code):
    link = reverse("users:email_verify", kwargs={"email": user_email, "code": code})
    full_link = f"{settings.DOMAIN_NAME}{link}"
    subjects = f"Подтверждение учетной записи для {user_email}"
    message = "Для подтверждения электронной почты {} перейдите по ссылке: {}.".format(
        user_email,
        full_link,
    )
    send_mail(
        subject=subjects,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
    )


def is_expired(self):
    if now() >= self.expiration:
        self.delete()
        self.save()
        return True
    return False


# VIEWS
class EmailVerificationHandler:
    def __init__(self, code, email):
        self.code = code
        self.email = email

    def proccess_email_verification(self):
        from users.models import EmailVerifications, Users

        user = get_object_or_404(Users, email=self.email)
        email_verifications = EmailVerifications.objects.filter(
            code=self.code, user=user
        )
        try:
            if (
                email_verifications.exists()
                and not email_verifications.last().is_expired()
            ):
                user.is_verified_email = True
                user.save()
                return True, user
            return False
        except Exception as e:
            return False


def check_last_first_name(request):
    if "first_name" not in request.data or "last_name" not in request.data:
        return True
    return False


def user_update_first_last_name(user_id, request):
    from users.models import Users

    user = get_object_or_404(Users, id=user_id)
    user.first_name = request.data["first_name"]
    user.last_name = request.data["last_name"]
    user.save()
